// assignments
var categoryList = document.getElementById("categoryList")


// testing assignments
var exampleOptions=["test", "programming"]; // TODO: Connect to backend and get categories from SQL

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

// Get categories for questions (Self-Invoking function)
(function() {
  exampleOptions.forEach(function (item) {
    var option = document.createElement("option");
    option.value = item;
    categoryList.appendChild(option);
  })
})();

//window.addEventListener('load', getOptions);