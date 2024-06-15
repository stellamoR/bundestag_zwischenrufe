const API_KEY = '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';
const FINE_TUNED_MODEL = 'ft-your-fine-tuned-model-id'; // Replace with your actual fine-tuned model ID

// Function to predict interruption
async function predictInterruption(text) {
  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: FINE_TUNED_MODEL,
        messages: [{ role: 'user', content: `Where is the interruption most likely in the following text? ${text}` }],
        max_tokens: 50,
        temperature: 0.5
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Error in predicting interruption: ${errorData.error.message}`);
    }

    const data = await response.json();
    return data.choices[0].message.content.trim();
  } catch (error) {
    console.error('Error in prediction:', error);
    return 'An error occurred while predicting the interruption.';
  }
}

// Event listener for the fine-tuning button
document.querySelector('#fineTuneButton').addEventListener('click', async () => {
  try {
    const prepareResponse = await fetch('/prepare-training-data');
    if (!prepareResponse.ok) {
      throw new Error(`Error in prepare-training-data: ${await prepareResponse.text()}`);
    }
    const fineTuneResponse = await fetch('/fine-tune-model', { method: 'POST' });
    if (!fineTuneResponse.ok) {
      throw new Error(`Error in fine-tune-model: ${await fineTuneResponse.text()}`);
    }
    alert('Fine-tuning process completed successfully.');
  } catch (error) {
    console.error('Error initiating fine-tune:', error);
    alert('An error occurred while fine-tuning the model. Please check the console for more details.');
  }
});

// Existing code for handling message submission
const submitButton = document.querySelector('#submit');
const outPutElement = document.querySelector('#output');
const inputElement = document.querySelector('input');
const historyElement = document.querySelector('.history');
const buttonElement = document.querySelector('button');

function changeInput(value) {
  inputElement.value = value;
}

async function getMessage(retryCount = 0, backoff = 1000) {
  console.log('clicked');
  const options = {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: inputElement.value }],
      max_tokens: 10
    })
  };

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", options);

    if (response.status === 429) {
      let retryAfter = parseInt(response.headers.get('Retry-After'));
      if (isNaN(retryAfter)) {
        retryAfter = backoff;
      } else {
        retryAfter *= 1000;
        retryAfter += 100;
      }
      if (retryCount >= 5) {
        throw new Error('Max retry attempts reached');
      }
      console.log(`Rate limited. Retrying after ${retryAfter / 1000} seconds...`);
      setTimeout(() => {
        getMessage(retryCount + 1, backoff * 2);
      }, retryAfter);
      return;
    }

    const data = await response.json();
    console.log(data);
    outPutElement.textContent = data.choices[0].message.content.slice(0, 10);
    if (data.choices[0].message.content && inputElement.value) {
      const pElement = document.createElement('p');
      pElement.textContent = inputElement.value;
      pElement.addEventListener('click', () => changeInput(pElement.textContent));
      historyElement.append(pElement);
    }
  } catch (error) {
    console.error(error);
  }
}

submitButton.addEventListener('click', getMessage);

function clearInput() {
  inputElement.value = '';
}

buttonElement.addEventListener('click', clearInput);

// Event listener for the predict interruption button
const predictButton = document.querySelector('#predictButton');
const inputTextElement = document.querySelector('#inputText');

predictButton.addEventListener('click', async () => {
  const text = inputTextElement.value;
  const prediction = await predictInterruption(text);
  document.querySelector('#output').textContent = prediction;
});
