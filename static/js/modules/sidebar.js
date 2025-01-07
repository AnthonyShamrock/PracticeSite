export default (function() {
    fetch("static/element/sidebarNav.html")
      .then(r=>r.text())
      .then(data=> {        
        // Load Sidebar
        document.querySelector(".sidebarNav").innerHTML = data

        // Highlight correct tab!
        const sidebarCollection = document.querySelector(".sidebarNav").children
        for (let i = 0; i < sidebarCollection.length; i++) {
            if (sidebarCollection[i].href == document.baseURI) {
                sidebarCollection[i].className = "active"
            }
            else {
                sidebarCollection[i].className = ""
            }
        }
    })
})()