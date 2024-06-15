import express from 'express';
import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';
import FormData from 'form-data';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const app = express();
const port = 3000;

const API_KEY = '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';
const FINE_TUNED_MODEL = 'ft-your-fine-tuned-model-id';  // Replace with your actual fine-tuned model ID

// Get __dirname using fileURLToPath and dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Content-Security-Policy middleware
app.use((req, res, next) => {
  res.setHeader("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-eval'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;");
  next();
});

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Endpoint to prepare training data
app.get('/prepare-training-data', async (req, res) => {
  console.log("/prepare-training-data endpoint called");
  const inputJsonFilePath = path.join(__dirname, 'public', 'shorter_12_013_1991-03-12.json');
  const outputJsonlFilePath = path.join(__dirname, 'output.jsonl');

  // Log file paths to verify they are correct
  console.log('Input JSON file path:', inputJsonFilePath);
  console.log('Output JSONL file path:', outputJsonlFilePath);

  fs.readFile(inputJsonFilePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading JSON file:', err);
      return res.status(500).send('Error reading JSON file');
    }

    try {
      const entries = JSON.parse(data);
      const writeStream = fs.createWriteStream(outputJsonlFilePath, { flags: 'w' });

      entries.forEach((entry, index) => {
        const text = entry.text;
        const comments = entry.comments;
        let completion = "";

        if (comments && comments.length > 0) {
          comments.forEach(comment => {
            completion += `<interruption> ${comment.text} `;
          });
        }

        if (completion.trim() === "") {
          completion = "";
        }

        const jsonlEntry = {
          prompt: text,
          completion: completion.trim()
        };

        writeStream.write(JSON.stringify(jsonlEntry) + '\n');
      });

      writeStream.end();
      console.log('JSON file successfully processed');
      res.send('JSON file successfully processed');
    } catch (jsonParseError) {
      console.error('Error processing JSON file:', jsonParseError);
      return res.status(500).send('Error processing JSON file');
    }
  });
});

// Endpoint to fine-tune the model
app.post('/fine-tune-model', async (req, res) => {
  console.log("/fine-tune-model endpoint called");
  const trainingDataPath = path.join(__dirname, 'output.jsonl');

  // Log the path to the training data file to verify it is correct
  console.log('Training data file path:', trainingDataPath);

  try {
    // Ensure the file exists before proceeding
    if (!fs.existsSync(trainingDataPath)) {
      console.error('Training data file does not exist:', trainingDataPath);
      return res.status(500).send('Training data file does not exist');
    }

    const fileData = fs.readFileSync(trainingDataPath, 'utf-8');
    
    // Upload the training data
    const formData = new FormData();
    formData.append('file', fs.createReadStream(trainingDataPath));
    formData.append('purpose', 'fine-tune');

    const uploadResponse = await fetch('https://api.openai.com/v1/files', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`
      },
      body: formData
    });

    if (!uploadResponse.ok) {
      const errorData = await uploadResponse.json();
      console.error('Error uploading training data:', errorData);
      throw new Error(`Error uploading training data: ${errorData.error.message}`);
    }

    const uploadData = await uploadResponse.json();
    const fileId = uploadData.id;

    // Fine-tune the model
    const fineTuneResponse = await fetch('https://api.openai.com/v1/fine-tunes', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        training_file: fileId,
        model: 'gpt-3.5-turbo',
        n_epochs: 4
      })
    });

    if (!fineTuneResponse.ok) {
      const errorData = await fineTuneResponse.json();
      console.error('Error fine-tuning model:', errorData);
      throw new Error(`Error fine-tuning model: ${errorData.error.message}`);
    }

    const fineTuneData = await fineTuneResponse.json();
    console.log('Fine-tune job created:', fineTuneData);
    res.send('Fine-tune job created');
  } catch (error) {
    console.error('Error during fine-tuning:', error);
    res.status(500).send('Error during fine-tuning: ' + error.message);
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
