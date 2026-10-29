document.addEventListener('DOMContentLoaded', function() {
    const typeFilter = document.getElementById('contentTypeFilter');
    const eventItems = document.querySelectorAll('.event-item');
    const popup = document.getElementById('eventPopup');
    const overlay = document.getElementById('overlay');
    const popupClose = document.getElementById('eventPopupClose');
    const popupName = document.getElementById('popupEventName');
    const popupStart = document.getElementById('popupEventStart');
    const popupEnd = document.getElementById('popupEventEnd');
    const popupDeadline = document.getElementById('popupEventDeadline');
    const popupURL = document.getElementById('popupEventURL');
    const popupDescription = document.getElementById('popupEventDescription');
    const popupStatus = document.getElementById('popupEventStatus');
    const popupAddress = document.getElementById('popupEventAddress');
    const popupContact = document.getElementById('popupEventContact');

    function applyFilters() {
        const selectedType = typeFilter.value;

        eventItems.forEach(item => {
            const itemType = item.dataset.type || "";
            const typeMatch = !selectedType || itemType === selectedType;
            item.style.display = typeMatch ? '' : 'none';
        });
    }

    if (typeFilter) {
        typeFilter.addEventListener('change', applyFilters);
    }

    document.querySelectorAll('.event-link').forEach(link => {
        link.addEventListener('click', function() {
            const name = this.getAttribute('data-name');
            const description = this.getAttribute('data-description') || "No description available.";
            popupStart.textContent = this.dataset.start || 'N/A';
            popupEnd.textContent = this.dataset.end || 'N/A';
            popupDeadline.textContent = this.dataset.deadline || 'N/A';
            popupStatus.textContent = this.dataset.status || 'N/A';
            popupName.textContent = name;
            popupDescription.textContent = description;
            popup.style.display = 'block';
            overlay.style.display = 'block';

            const url = this.dataset.url;
            if (url) {
                popupURL.innerHTML = `<a href="${url}" target="_blank" rel="noopener noreferrer" class="link">${url}</a>`;
            } else {
                popupURL.textContent = 'N/A';
            }

            const addrParts = [this.dataset.address1, this.dataset.address2, this.dataset.city, this.dataset.state, this.dataset.postal].filter(Boolean);
            popupAddress.textContent = addrParts.length ? addrParts.join(', ') : 'N/A';
            const contactParts = [this.dataset.contactName, this.dataset.contactPhone, this.dataset.contactEmail].filter(Boolean);
            popupContact.textContent = contactParts.length ? contactParts.join(' | ') : 'N/A';
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

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            popup.style.display = 'none';
            overlay.style.display = 'none';
        }
    });
});
