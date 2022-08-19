// Select id based on past workout
let workout = Object.keys(history);
let num = workout.length % 6 ? workout.length % 6 : 6;
let id = 'day' + num;

// Make tab active
let tab = document.getElementById(id);
tab.classList.add('active');

// Make tab content active
let tabPane = document.getElementById(id + '-link');
tabPane.classList.add('active');

// Get button by id
let button = document.getElementById('btn');

// Appear when scroll to bottom
window.onscroll = function() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    button.style.display = 'block';
  } else {
    button.style.display = 'none';
  }
}

// Go to top on mouse click
button.onclick = function() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}