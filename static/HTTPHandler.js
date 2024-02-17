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
