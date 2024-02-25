// assignments

// HTTP handler
async function postData(url="", data={}, formData=false) {
  if (formData) {
    const response = await fetch(url, {
      method: 'POST',
       headers: {
         'Content-Type': 'application/x-www-form-urlencoded'
       },
        body: new URLSearchParams(new FormData(data))
    });
    return response.json();
  }
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

// OLD: Get categories for questions (Self-Invoking function)
/*(function() {
  exampleOptions.forEach(function (item) {
    var option = document.createElement("option");
    option.value = item;
    categoryList.appendChild(option);
  })
})();*/

getData("/user/currentUser")
  .then(payload => {
    if (!payload.Success) {
      return location.href = "/login"
    }
  })
  .catch(()=>{})

function toggleErrorLabel(status=false, message=null) {
  if (message) {
    document.getElementById('errorlabel').textContent = message
  }
  if (status) {
    document.getElementById('errorlabel').removeAttribute('hidden')
    setTimeout(toggleErrorLabel, 5000)
  }
  else {
    document.getElementById('errorlabel').setAttribute('hidden', "")
  }
  return true
}

// Get categories for questions (Self-Invoking function)
(function() {
  getData("/question/categories")
    .then(payload => {
      if (payload.Success) {
        payload["Categories"].forEach(function (item) {
          document.getElementById("categoryList").options.add(new Option(item, item));
        })
      }
    })
    .catch(()=>{
      document.getElementById("categoryList").options.add(new Option("ERROR"));
    })
})();

document.getElementById("addQuestionForm").addEventListener("submit", event => {
  event.preventDefault();
  postData("/question/add", document.getElementById("addQuestionForm"), true)
  .then(r=>{
    toggleErrorLabel(true, r.Message)
  })
  .catch(()=>{
    toggleErrorLabel(true, "Error Occured!")
  })
});

//window.addEventListener('load', getOptions);