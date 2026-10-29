// "Show password" icon and function
let eyeicon = document.getElementById("eyeicon");
let password = document.getElementById("password");

if (eyeicon && password) {
    eyeicon.onclick = function() {
        if (password.type == "password") {
            password.type = "text";
            eyeicon.src = eyeicon.dataset.eyeOpen;
        } else {
            password.type = "password";
            eyeicon.src = eyeicon.dataset.eyeClosed;
        }
    };
}
