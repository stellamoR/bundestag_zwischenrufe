const API_Key = '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'
const submitButton = document.querySelector('#submit')
const outPutElement = document.querySelector('#output')
const inputElement = document.querySelector('input')
const historyElement = document.querySelector('.history')
const buttonElement = document.querySelector('button')


function changeInput(value)
{
    inputElement.value = value
}

async function getMessage(retryCount = 0, backoff = 1000) {
    console.log('clicked')
    const options = {
        method: 'POST',
        headers:{
            'Authorization' : `Bearer ${API_Key}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model:"gpt-3.5-turbo",
            messages: [{role:"user", content: inputElement.value}],
            max_tokens: 10
        })
    }

    try {
        const response = await fetch("https://api.openai.com/v1/chat/completions", options)

        if (response.status === 429) {
            let retryAfter = parseInt(response.headers.get('Retry-After'));
            if (isNaN(retryAfter)) {
              // Fallback to default backoff value
              retryAfter = backoff;
            } else {
              // Add a small buffer to the retryAfter value
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

        const data = await response.json()
        console.log(data)
        outPutElement.textContent = data.choices[0].message.content.slice(0, 10)
        if(data.choices[0].message.content && inputElement.value) {
            const pElement = document.createElement('p')
            pElement.textContent = inputElement.value
            pElement.addEventListener('click', () => changeInput(pElement.textContent))
            historyElement.append(pElement)
        }
    }
    catch (error) {
        console.error(error)
    }
    
}
submitButton.addEventListener('click', getMessage)

function clearInput() {
    inputElement.value = ''
}

buttonElement.addEventListener('click', clearInput)


