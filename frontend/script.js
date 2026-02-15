function login(username, password) {
  fetch(`http://localhost:8000/login?login=${username}&password=${password}`)
}
