export async function postData(url="", data={}) {

  // Handle formdata
  if (data instanceof HTMLFormElement) {
    return (await fetch(url, {
      method: 'POST',
       headers: {
         'Content-Type': 'application/x-www-form-urlencoded'
       },
        body: new URLSearchParams(new FormData(data))
    })).json()
  }

  return (await fetch(url, {
    method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })).json()
}

export async function getData(url="") { // make this work URL data
  return (await fetch(url)).json()
  //const response = await fetch(url);
  //return response.json();
}
