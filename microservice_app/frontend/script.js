async function login() {
  username = document.getElementById("username").value
  password = document.getElementById("password").value


  response = await fetch(`http://localhost:8000/login?username=${username}&password=${password}`, {
    method: "POST"
  })

  const data = await response.json()

  if (data.status == "success") {
    console.log("logged in")
    localStorage.setItem("jwt", data.jwt)
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

  response = await fetch(`http://localhost:8000/register?username=${username}&password=${password}&email=${email}`, {
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
  jwt = localStorage.getItem("jwt")
  response = await fetch(`http://localhost:8000/logout?user_token=${jwt}`, {
    method: "POST"
  })

  data = await response.json()

  if (data.status == "success") {
    localStorage.removeItem("jwt")
  } else {
    alert("Somthing went wrong. Please try again later")
  }
}

async function get_messages() {
  jwt = localStorage.getItem("jwt")
  user2_id = document.getElementById("user2_id").value
  response = await fetch(`http://localhost:8000/read_messages?user_token=${jwt}&user2_id=${user2_id}`, {
    method: "GET"
  })
  messages = await response.json()

  if (message == []) {
    return 
  }

  for (message of messages) {
    p_elem = document.createElement("p")
    p_elem.textContent = message
    document.body.appendChild(p_elem)
  }
}

async function send_message() {
  jwt = localStorage.getItem("jwt")
  message = document.getElementById("message_input").value
  receiver_id = document.getElementById("user2_id").value
  response = await fetch(`http://localhost:8000/send_message?user_token=${jwt}&receiver_id=${receiver_id}&text=${message}`, {
    method: "POST"
  })

}

window.onload = async function () {
  jwt = localStorage.getItem("jwt")

  if (!jwt) {
    window.location.replace = "/login.html"
    return
  }

  response = await fetch(`http://localhost:8000/is_online?user_token=${jwt}`, {
    method: "GET"
  })

  data = await response.json()

  if (data.status == "offline") {
    localStorage.removeItem("jwt")
    window.location.replace("./login.html")
    return
  }
}