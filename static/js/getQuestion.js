// assignments
import {getData, postData} from "./modules/httpHandler.js"
import "./modules/sidebar.js" // Load Sidebar
var questionId = 0

// HTTP handler
/*async function postData(url="", data={}) {
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
}*/


// Get new question and display it!
function getQuestion() {
  getData("/question/get")
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
  postData("/question/submit", {id: questionId, answer: answer})
  .then(payload => {
    alert(payload.Message)
    getQuestion()
  })
  /*
  const response = await fetchS('/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    JSON: JSON.stringify({ id: questionId, answer: answer })
  });
  
  const result = await response.text();

  // Display result to user
  alert(result)*/
  //getQuestion()
});

window.addEventListener('load', getQuestion);