// Day of week
let dow = {
  0: 'day1',
  1: 'day1',
  2: 'day2',
  3: 'day3',
  4: 'day4',
  5: 'day5',
  6: 'day6'
};

// Select id based on day of week
let today = new Date();
//let id = dow[today.getDay()];
let id = 'day2';

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

// 2022-08-01: push
// 2022-08-02: pull
// 2022-08-03: legs
// 2022-08-04: push
// 2022-08-05: pull
// 2022-08-13: legs
// 2022-08-15: push
// 2022-08-18: pull (tbc)