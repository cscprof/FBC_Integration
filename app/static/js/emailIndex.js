// Separates email verification into two separate steps: a "request verification" page and a "send token" page
function showEmailStep() {
  document.getElementById("requestStep").style.display = "none";
  document.getElementById("emailStep").style.display = "block";
}
