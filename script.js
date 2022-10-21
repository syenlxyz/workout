// Assign workout to day of week
let workout = {
  0: 'push',
  1: 'push',
  2: 'pull',
  3: 'legs',
  4: 'push',
  5: 'pull',
  6: 'legs'
}

// Select workout based on day of week
let today = new Date();
let dow = today.getDay();
let id = workout[dow];

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