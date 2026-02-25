async function login() {
  username = document.getElementById("username").value
  password = document.getElementById("password").value


  response = await fetch(`http://localhost:8000/login?username=${username}&password=${password}`, {
    method: "POST"
  })

  const data = await response.json()

  if (data.status == "success") {
    console.log("logged in")
    localStorage.setItem("user_id", data.user_id)
    window.location.replace("./index.html") 
  } else {
    console.log("Failed to log in")
    alert(data.detail)
  }
}

async function register(username, password, email) {
  username = document.getElementById("username").value
  password = document.getElementById("password").value
  email = document.getElementById("email").value

  response = await fetch(`http://localhost:8000/register?username=${username}&password=${password}&email=${email}`,{
      method: "POST"
  })

  const data = await response.json()

  if (data.status == "success") {
    window.location.replace("./login.html") 
  } else {
    alert(response.detail)
  }
}

async function logout() {
  user_id = localStorage.getItem("user_id")
  response = await fetch(`http://localhost:8000/logout?user_id=${user_id}`, {
    method: "POST"
  })

  data = await response.json()

  if (data.status == "success") {
    localStorage.removeItem("user_id")
  } else {
    alert("Somthing went wrong. Please try again later")
  }
}

window.onload = async function () {
  user_id = localStorage.getItem("user_id")

  if (!user_id) {
    window.location.replace = "/login.html"
    return
  }

  response = await fetch(`http://localhost:8000/is_online?user_id=${user_id}`,{
    method: "GET"
  })  

  data = await response.json()

  if (data.status == "offline") {
    localStorage.removeItem("user_id")
    window.location.replace("./login.html") 
    return
  } else if (data.status == "online") {

  }
}