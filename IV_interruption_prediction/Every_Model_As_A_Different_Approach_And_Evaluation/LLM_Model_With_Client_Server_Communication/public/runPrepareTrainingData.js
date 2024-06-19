const fs = require('fs');
const path = require('path');

// Function to prepare training data from JSON to JSONL
async function prepareTrainingData() {
  const inputJsonFilePath = 'C:\\Users\\eddi6\\OneDrive\\Desktop\\NLP_LLM\\shorter_12_013_1991-03-12.json';
  const outputJsonlFilePath = path.join(__dirname, 'output.jsonl');

  fs.readFile(inputJsonFilePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading JSON file:', err);
      return;
    }

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
  });
}

prepareTrainingData();
