document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  const popup = document.getElementById('eventPopup');
  const overlay = document.getElementById('overlay');
  const filterSelect = document.getElementById('contentTypeFilter');

  let allEvents = []; 

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    themeSystem: 'standard',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek,multiMonthYear'
    },
    views: { listWeek: { buttonText: 'list' } },
    contentHeight: 'auto',
    events: [], 
    eventClick: function(info) {
      popup.innerHTML = `
        <span id="eventPopupClose">X</span>
        <h3>${info.event.title}</h3>
        <p><strong>Start:</strong> ${info.event.start.toLocaleString()}</p>
        <p><strong>End:</strong> ${info.event.end.toLocaleString()}</p>
        <p><strong>Description:</strong> ${info.event.extendedProps.description || "N/A"}</p>
        <p><strong>URL:</strong> <a href="${info.event.url}" classname="link" target="_blank">${info.event.url || "N/A"}</a></p>
      `;
      popup.style.display = 'block';
      overlay.style.display = 'block';
      info.jsEvent.preventDefault();

      document.getElementById('eventPopupClose').onclick = function() {
        popup.style.display = 'none';
        overlay.style.display = 'none';
      };
      overlay.onclick = function() {
        popup.style.display = 'none';
        overlay.style.display = 'none';
      };
    }
  });

  fetch('/approved-events')
    .then(res => res.json())
    .then(data => {
      allEvents = data;
      calendar.addEventSource(allEvents);
    })
    .catch(err => console.error(err));

  filterSelect.addEventListener('change', function() {
    const selectedType = filterSelect.value;

    const filteredEvents = selectedType
      ? allEvents.filter(e => String(e.content_type) === selectedType)
      : allEvents;

    calendar.removeAllEvents();
    calendar.addEventSource(filteredEvents);
  });

  calendar.render();
});
