const form = document.getElementById('questionForm');

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
    body: JSON.stringify({ id: 1, answer: answer }) // Change id value accordingly
  });
  
  const result = await response.text();
  // Display result to user
  console.log(result);
});

window.addEventListener('load', async () => {
  const response = await fetch('/get');
  const question = await response.text();
  console.log(response)
  //document.getElementById('questionLabel').textContent = question;
});