console.log("calendar.js loaded!");
// references to DOM elements
const daysContainer = document.getElementById("days");
const monthYear = document.getElementById("monthYear");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

// date object to track the current displayed month
let currentDate = new Date();


function renderCalendar() {
  // start of the month
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  // set month & year title
  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  monthYear.textContent = `${monthNames[month]} ${year}`;

  // get first and last day of the month
  const firstDay = new Date(year, month, 1).getDay();
  const lastDate = new Date(year, month + 1, 0).getDate();

  // get last date of previous month
  const prevLastDate = new Date(year, month, 0).getDate();

  // clear previous days
  daysContainer.innerHTML = "";

  // fill in the blanks for the previous month
  for (let i = firstDay; i > 0; i--) {
    const div = document.createElement("div");
    div.classList.add("prev-date");
    div.textContent = prevLastDate - i + 1;
    div.style.opacity = "0.3";
    daysContainer.appendChild(div);
  }

  // fill in current month’s days
  for (let day = 1; day <= lastDate; day++) {
    const div = document.createElement("div");
    div.textContent = day;

    const today = new Date();
    if (
      day === today.getDate() &&
      month === today.getMonth() &&
      year === today.getFullYear()
    ) {
      div.classList.add("today");
    }

    // click event for each day
    div.addEventListener("click", () => {
      document.querySelectorAll(".days div").forEach(d => d.classList.remove("selected"));
      div.classList.add("selected");
      console.log(`clicked ${monthNames[month]} ${day}, ${year}`);
    });

    daysContainer.appendChild(div);
  }

  // fill next month’s overflow days to complete the grid
  const totalCells = daysContainer.children.length;
  const nextDays = 42 - totalCells;
  for (let j = 1; j <= nextDays; j++) {
    const div = document.createElement("div");
    div.textContent = j;
    div.classList.add("next-date");
    div.style.opacity = "0.3";
    daysContainer.appendChild(div);
  }
}

// navigation
prevBtn.addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() - 1);
  renderCalendar();
});

nextBtn.addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() + 1);
  renderCalendar();
});

// initialize
renderCalendar();