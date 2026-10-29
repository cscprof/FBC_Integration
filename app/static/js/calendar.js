document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  if (!calendarEl) return;

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
      const ep = info.event.extendedProps;
      const addr = [ep.event_address1, ep.event_address2, ep.event_city, ep.event_state, ep.event_postal_code].filter(Boolean).join(', ');
      const schoolsList = ep.schools && ep.schools.length > 0 ? ep.schools.join(', ') : 'N/A';
      popup.innerHTML = `
        <span id="eventPopupClose">X</span>
        <h3>${info.event.title}</h3>
        <p><strong>Content Type:</strong> ${ep.tag || "N/A"}</p>
        <p><strong>Schools:</strong> ${schoolsList}</p>
        <p><strong>Start:</strong> ${info.event.start.toLocaleString()}</p>
        <p><strong>End:</strong> ${info.event.end.toLocaleString()}</p>
        <p><strong>Registration Deadline:</strong> ${ep.registration_deadline
        ? new Date(ep.registration_deadline).toLocaleString()
        : 'N/A'}</p>
        <p><strong>Description:</strong> ${ep.description || "N/A"}</p>
        <p><strong>Address:</strong> ${addr || "N/A"}</p>
        <p><strong>Contact:</strong> ${ep.contact_name || "N/A"}${ep.contact_phone ? ' | ' + ep.contact_phone : ''}${ep.contact_email ? ' | ' + ep.contact_email : ''}</p>
        <p><strong>URL:</strong> <a href="${info.event.url}" class="link" target="_blank">${info.event.url || "N/A"}</a></p>
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
      
      // Check if an event was passed as a query parameter
      const urlParams = new URLSearchParams(window.location.search);
      const eventParam = urlParams.get('event');
      
      if (eventParam) {
        // Find the event with matching title
        const targetEvent = allEvents.find(e => e.title === decodeURIComponent(eventParam));
        if (targetEvent) {
          // Wait a moment for the calendar to render, then show the popup
          setTimeout(() => {
            const tAddr = [targetEvent.event_address1, targetEvent.event_address2, targetEvent.event_city, targetEvent.event_state, targetEvent.event_postal_code].filter(Boolean).join(', ');
            popup.innerHTML = `
              <span id="eventPopupClose">X</span>
              <h3>${targetEvent.title}</h3>
              <p><strong>Start:</strong> ${new Date(targetEvent.start).toLocaleString()}</p>
              <p><strong>End:</strong> ${new Date(targetEvent.end).toLocaleString()}</p>
              <p><strong>Registration Deadline:</strong> ${targetEvent.registration_deadline
              ? new Date(targetEvent.registration_deadline).toLocaleString()
              : 'N/A'}</p>
              <p><strong>Description:</strong> ${targetEvent.description || "N/A"}</p>
              <p><strong>Address:</strong> ${tAddr || "N/A"}</p>
              <p><strong>Contact:</strong> ${targetEvent.contact_name || "N/A"}${targetEvent.contact_phone ? ' | ' + targetEvent.contact_phone : ''}${targetEvent.contact_email ? ' | ' + targetEvent.contact_email : ''}</p>
              <p><strong>URL:</strong> <a href="${targetEvent.url}" class="link" target="_blank">${targetEvent.url || "N/A"}</a></p>
            `;
            popup.style.display = 'block';
            overlay.style.display = 'block';
            
            document.getElementById('eventPopupClose').onclick = function() {
              popup.style.display = 'none';
              overlay.style.display = 'none';
            };
            overlay.onclick = function() {
              popup.style.display = 'none';
              overlay.style.display = 'none';
            };
          }, 500);
        }
      }
    })
    .catch(err => console.error(err));

  const schoolFilter = document.getElementById('schoolFilter');

  function applyFilters() {
    const selectedType = filterSelect.value;
    const selectedSchool = schoolFilter.value;

    const filteredEvents = allEvents.filter(e => {
      const typeMatch = !selectedType || e.tag === selectedType;
      const schoolMatch = !selectedSchool || (e.schools && e.schools.includes(selectedSchool));
      return typeMatch && schoolMatch;
    });

    calendar.removeAllEvents();
    calendar.addEventSource(filteredEvents);
  }

  filterSelect.addEventListener('change', applyFilters);
  schoolFilter.addEventListener('change', applyFilters);

  calendar.render();
});
