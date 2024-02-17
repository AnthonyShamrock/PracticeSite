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

async function getData(url="") {
  const response = await fetch(url);
  return response.json();
}

// Check if user is developer; if not then return.
function init() {
  if (sessionStorage.getItem("IsDeveloper")) {
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
if (sessionStorage.getItem("IsDeveloper") != true){location.replace(window.location.origin)} else {document.getElementById("html").removeAttribute("hidden")}

// Get new question and display it
function getQuestion() {
  getData("/get")
  .then(
    payload =>{
    questionId = payload.id;
    document.getElementById('questionLabel').textContent = payload.question;
  })
}

document.getElementById('questionForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const answer = document.getElementById('questionAnswerField').value;

  if (answer === null) {
    return
  }
  postData("/submit", {id: questionId, answer: answer})
  .then(payload => {alert(payload)})

  // Display result to user
  getQuestion()
});

window.addEventListener('load', getQuestion);