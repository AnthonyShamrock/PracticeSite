var questionId = 0

// HTTP handler
async function postData(url="", data={}) {
  const response = await fetch(url, {
    method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  });
  return response.json();
}

async function getData(url="", data={}) {
  const response = await fetch(url, {
    method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  });
  return response.json();
}


// Get new question and display it!
async function getQuestion() {
  const response = await fetch('/get');
  const payload = JSON.parse(await response.text());
  questionId = payload.id
  document.getElementById('questionLabel').textContent = payload.question;
}

document.getElementById('questionForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const answer = document.getElementById('questionAnswerField').value;

  if (answer === null) {
    return
  }
  const response = await fetch('/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    JSON: JSON.stringify({ id: questionId, answer: answer })
  });
  
  const result = await response.text();

  // Display result to user
  alert(result)
  getQuestion()
});

window.addEventListener('load', getQuestion);