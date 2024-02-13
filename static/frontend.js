const form = document.getElementById('questionForm');
var questionId = 0

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const answer = document.getElementById('questionAnswerField').value;

  console.log(answer)
  if (answer === null) {
    return
  }
  const response = await fetch('/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: questionId, answer: answer }) // Change id value accordingly
  });
  
  const result = await response.text();
  // Display result to user
  alert(result)
  location.reload()
});

window.addEventListener('load', async () => {
  const response = await fetch('/get');
  const payload = JSON.parse(await response.text());
  questionId = payload.id
  document.getElementById('questionLabel').textContent = payload.question;
});