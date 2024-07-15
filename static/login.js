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

async function hash(text) {
  return await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)).then(hashbuffer => {
    return Array.from(new Uint8Array(hashbuffer)).map((b) => b.toString(16).padStart(2, '0')).join('');
  })
};


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

document.getElementById("login").addEventListener("submit", async event => {
  event.preventDefault();
  // if fail revert to this text
  revertText = document.getElementsByName('Password')[0].value

  // hash password for transport
  await hash(document.getElementsByName('Password')[0].value)
    .then(e=>{
      document.getElementsByName('Password')[0].value = e
    })
  
  // Submit passwokrd
  postData("/user/login", document.getElementById("login"), true)
  .then(r=>{
    if (r["Success"]) {
      if (document.referrer != '') {
        return history.back()
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
  document.getElementsByName('Password')[0].value = revertText
  revertText = null
});