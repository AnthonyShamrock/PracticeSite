var questionId = 0

import {getData, postData} from "./modules/httpHandler.js"
import "./modules/sidebar.js" // Load Sidebar

//loadSidebarNav()
// Check if user is developer; if not then return.
getData("/user/currentUser")
  .then((r)=>{
    if (r["Success"] & r["Username"]=="admin") {
      document.getElementsByName("html").removeAttribute("hidden")
    }
    else {
      console.log("Failed", getData("/user/currentUser"));
      location.replace("/login");
    }
  })
  .catch((e) => {})

// Get new question and display it
function getQuestion() {
  getData("/question/get")
  .then(
    payload =>{
    questionId = payload.id;
    //document.getElementById('questionLabel').textContent = payload.question;
  })
}

/*document.getElementById('questionForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const answer = document.getElementById('questionAnswerField').value;

  if (answer === null) {
    return
  }
  postData("/submit", {id: questionId, answer: answer})
  .then(payload => {alert(payload)})

  // Display result to user
  getQuestion()
});*/

window.addEventListener('load', getQuestion);