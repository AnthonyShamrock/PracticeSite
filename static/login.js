var questionId = 0

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

function toggleErrorLabel(status=false) {
  if (status) {
    document.getElementById('errorlabel').removeAttribute('hidden')
    setTimeout(toggleErrorLabel, 5000)
  }
  else {
    document.getElementById('errorlabel').setAttribute('hidden', "")
  }
  return true
}

document.getElementById("login").addEventListener("submit", event => {
  event.preventDefault();
  postData("/user/login", document.getElementById("login"), true)
  .then(r=>{
    console.log(r)
    if (r["Success"]) {
      if (document.referrer != '') {
        history.back()
      }
      location.replace("/")
    }
    else {
      toggleErrorLabel(true)
      
    }
  })
  .catch(()=>{
    toggleErrorLabel(true)
  })
  //return false
  //document.getElementsByName("Username"))[0].Value
});