document.addEventListener('DOMContentLoaded', function() {
    const popup = document.getElementById('eventPopup');
    const overlay = document.getElementById('overlay');
    const popupClose = document.getElementById('eventPopupClose');
    const popupName = document.getElementById('popupEventName');
    const popupDescription = document.getElementById('popupEventDescription');

    document.querySelectorAll('.event-link').forEach(link => {
        link.addEventListener('click', function() {
            const name = this.getAttribute('data-name');
            const description = this.getAttribute('data-description') || "No description available.";
            popupName.textContent = name;
            popupDescription.textContent = description;
            popup.style.display = 'block';
            overlay.style.display = 'block';
        });
    });

    popupClose.addEventListener('click', function() {
        popup.style.display = 'none';
        overlay.style.display = 'none';
    });

    overlay.addEventListener('click', function() {
        popup.style.display = 'none';
        overlay.style.display = 'none';
    });
});
