document.addEventListener('DOMContentLoaded', function () {
    const typeFilter = document.getElementById('contentTypeFilter');
    const schoolFilter = document.getElementById('schoolFilter');
    const eventItems = document.querySelectorAll('.event-item');

    function applyFilters() {
        const selectedType = typeFilter.value;
        const selectedSchool = schoolFilter.value;

        eventItems.forEach(item => {
            const itemType = item.dataset.type || "";
            const itemSchools = item.dataset.schools ? JSON.parse(item.dataset.schools) : [];

            const typeMatch = !selectedType || itemType === selectedType;
            const schoolMatch = !selectedSchool || itemSchools.includes(selectedSchool);

            item.style.display = (typeMatch && schoolMatch) ? '' : 'none';
        });
    }

    typeFilter.addEventListener('change', applyFilters);
    schoolFilter.addEventListener('change', applyFilters);
});
