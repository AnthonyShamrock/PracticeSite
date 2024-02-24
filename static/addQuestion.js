// assignments
var categoryList = document.getElementById("categoryList")


// testing assignments
var exampleOptions=["test", "programming"]; // TODO: Connect to backend and get categories from SQL

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

// Get categories for questions (Self-Invoking function)
(function() {
  exampleOptions.forEach(function (item) {
    categoryList.options.add(new Option(item, item));
  })
})();

document.getElementById("addQuestionForm").addEventListener("submit", event => {
  event.preventDefault();
  postData("/question/add", document.getElementById("addQuestionForm"), true)
  .then(r=>{
    console.log(r)
  })
  .catch(()=>{
    console.log("ERROR")
  })
});

//window.addEventListener('load', getOptions);