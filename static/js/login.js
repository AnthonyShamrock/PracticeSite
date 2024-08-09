import {getData, postData} from "./modules/httpHandler.js"
import "./modules/sidebar.js" // Load Sidebar

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
  // hash password for transport
  await hash(event.target.elements.Password.value)
    .then(e=>{
      event.target.elements.Password.value = e
    })
  // Submit password
  postData("/user/login", event.target)
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
  document.getElementsByName('Password')[0].value = ""
});