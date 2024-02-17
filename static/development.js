var questionId = 0

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

// Check if user is developer; if not then return. 
function init() {
  if (!sessionStorage.getItem("IsDeveloper")) {
    postData("/isDeveloper", {secret: prompt("You are entering the development area! Please enter the password.")})
    .then((r) =>{
      if (r["Success"] == true) {
        sessionStorage.setItem("IsDeveloper", true)
        location.replace(window.location.href)
      }
      else {
        location.replace(window.location.origin)
      }
    })
  }
  return true
}
init()
if (!sessionStorage.getItem("IsDeveloper")){location.replace(window.location.origin)} else {document.getElementById("html").removeAttribute("hidden")}

// Get new question and display it
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
    body: JSON.stringify({ id: questionId, answer: answer })
  });
  
  const result = await response.text();

  // Display result to user
  alert(result)
  getQuestion()
});

window.addEventListener('load', getQuestion);