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

async function getData(url="") { // make this work URL data
  const response = await fetch(url);
  return response.json();
}

// Check if user is developer; if not then return.
getData("/user/currentUser")
  .then((r)=>{
    if (r["Success"] & r["Username"]=="admin") {
      document.getElementById("html").removeAttribute("hidden")
    }
    else {
      console.log("Failed", getData("/user/currentUser"));
      location.replace("/login");
    }
  })
  .catch((e) => {})

// Get new question and display it
function getQuestion() {
  getData("/get/question")
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