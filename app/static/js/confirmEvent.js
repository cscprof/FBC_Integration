(function(){
  var seconds = 5;
  var el = document.getElementById('secs');
  var countdownEl = document.getElementById('countdown');
  var redirectUrl = (countdownEl && countdownEl.getAttribute('data-redirect-url')) || '/calendar';
  var timer = setInterval(function(){
    seconds -= 1;
    if(el) el.textContent = seconds;
    if(seconds <= 0){
      clearInterval(timer);
      window.location = redirectUrl;
    }
  }, 1000);
})();
