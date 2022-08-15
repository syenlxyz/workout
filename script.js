var dow = {
  0: 'day1',
  1: 'day1',
  2: 'day2',
  3: 'day3',
  4: 'day4',
  5: 'day5',
  6: 'day6'
};

var today = new Date();
var id = dow[today.getDay()];

var tab = document.getElementById(id);
tab.classList.add('active');

var tabPane = document.getElementById(id + '-link');
tabPane.classList.add('active');

// 2022-08-01: push
// 2022-08-02: pull
// 2022-08-03: legs
// 2022-08-04: push
// 2022-08-05: pull
// 2022-08-13: legs
// 2022-08-15: push
// 2022-08-16: pull (tbc)