function deleteResource() {
    const resourceId = document.getElementById('editResourceId').value;
    if (confirm('Are you sure you want to delete this resource?')) {
        const editForm = document.getElementById('editForm');
        const deleteTemplate = (editForm && editForm.getAttribute('data-delete-url-template')) || '/resources/delete/0';
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = deleteTemplate.replace('0', resourceId);
        document.body.appendChild(form);
        form.submit();
    }
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

const editFormEl = document.getElementById('editForm');
if (editFormEl) {
    editFormEl.addEventListener('submit', function () {
        const resourceId = document.getElementById('editResourceId').value;
        const editTemplate = this.getAttribute('data-edit-url-template') || '/resources/edit/0';
        this.action = editTemplate.replace('0', resourceId);
    });
}

function openEditModal(button) {
    document.getElementById('editResourceId').value = button.getAttribute('data-resource-id');
    document.getElementById('editTitle').value = button.getAttribute('data-title');
    document.getElementById('editUrl').value = button.getAttribute('data-url');
    document.getElementById('editCategory').value = button.getAttribute('data-category-id');
    document.getElementById('editName').value = button.getAttribute('data-name') || '';
    document.getElementById('editEmail').value = button.getAttribute('data-email') || '';
    document.getElementById('editPhone').value = button.getAttribute('data-phone') || '';
    document.getElementById('editModal').style.display = 'flex';
}

function filterAdminRows() {
    const searchValue = document.getElementById('adminSearchInput').value.toLowerCase();
    const selectedCategory = document.getElementById('adminCategorySelect').value;
    const rows = document.querySelectorAll('#adminResourceRows tr[data-category]');

    rows.forEach((row) => {
        const rowCategory = row.getAttribute('data-category');
        const rowSearchText = row.getAttribute('data-search').toLowerCase();
        const matchesSearch = rowSearchText.includes(searchValue);
        const matchesCategory = selectedCategory === 'all' || rowCategory === selectedCategory;
        row.style.display = matchesSearch && matchesCategory ? '' : 'none';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-resource-btn-inline').forEach((button) => {
        button.addEventListener('click', function () {
            openEditModal(this);
        });
    });

    document.getElementById('adminSearchInput').addEventListener('keyup', filterAdminRows);
    document.getElementById('adminCategorySelect').addEventListener('change', filterAdminRows);

    window.onclick = function (event) {
        const editModal = document.getElementById('editModal');
        const uploadModal = document.getElementById('uploadModal');
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
        if (event.target === uploadModal) {
            uploadModal.style.display = 'none';
        }
    };
});
