const loginButton = document.getElementById("loginButton");
const errorMessage = document.getElementById("errorMessage");

loginButton.addEventListener("click", () => {
const email = document.getElementById("email").value;
const password = document.getElementById("password").value;

const requestData = {
  email: email,
  password: password
};
fetch("/auth/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(requestData)
})
.then(response => {
  if (response.status === 204) {
    window.location.href = "/home";
  } else {
    errorMessage.style.display = "block";
    setTimeout(() => {
                errorMessage.style.display = "none";
            }, 2000);
  }
})
});
