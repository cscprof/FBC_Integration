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

function closeResourceInfoModal() {
    const modal = document.getElementById('resourceInfoModal');
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
}

function openResourceInfoModal(wrapper) {
    const title = wrapper.getAttribute('data-title') || 'Resource';
    const url = wrapper.getAttribute('data-url') || '';
    const categoryName = wrapper.getAttribute('data-category-name') || '-';
    const name = wrapper.getAttribute('data-name') || '';
    const email = wrapper.getAttribute('data-email') || '';
    const phone = wrapper.getAttribute('data-phone') || '';

    document.getElementById('resourceInfoTitle').innerText = title;
    document.getElementById('resourceInfoCategory').innerText = categoryName.charAt(0).toUpperCase() + categoryName.slice(1);

    const nameEl = document.getElementById('resourceInfoName');
    const emailEl = document.getElementById('resourceInfoEmail');
    const phoneEl = document.getElementById('resourceInfoPhone');
    const noContactEl = document.getElementById('resourceInfoNoContact');

    nameEl.innerText = name ? name : '';
    emailEl.innerText = email ? email : '';
    phoneEl.innerText = phone ? phone : '';
    const hasContact = Boolean(name || email || phone);
    noContactEl.style.display = hasContact ? 'none' : 'block';

    const link = document.getElementById('resourceInfoLink');
    link.href = url;
    link.style.pointerEvents = url ? 'auto' : 'none';
    link.style.opacity = url ? '1' : '0.5';

    const modal = document.getElementById('resourceInfoModal');
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
}

const editFormEl = document.getElementById('editForm');
if (editFormEl) {
    editFormEl.addEventListener('submit', function(e) {
        const resourceId = document.getElementById('editResourceId').value;
        const editTemplate = this.getAttribute('data-edit-url-template') || '/resources/edit/0';
        this.action = editTemplate.replace('0', resourceId);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector(".searchinput");
    const categorySelect = document.querySelector(".categoryselect");
    const resourceBoxes = document.querySelectorAll(".resource-card-wrapper");
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category');
    if (categoryParam) {
        categorySelect.value = categoryParam;
    }

    function filterResources() {
        const searchValue = searchInput.value.toLowerCase();
        const selectedCategory = categorySelect.value;

        resourceBoxes.forEach(box => {
            const boxCategory = box.getAttribute("data-category");
            const textContent = box.innerText.toLowerCase();

            const matchesSearch = textContent.includes(searchValue);

            if (matchesSearch) {
                box.style.display = "block";
            } else {
                box.style.display = "none";
            }
        });
    }

    function openEditModal(button) {
        const resourceId = button.getAttribute('data-resource-id');
        const title = button.getAttribute('data-title');
        const url = button.getAttribute('data-url');
        const categoryId = button.getAttribute('data-category-id');
        const name = button.getAttribute('data-name');
        const email = button.getAttribute('data-email');
        const phone = button.getAttribute('data-phone');

        document.getElementById('editResourceId').value = resourceId;
        document.getElementById('editTitle').value = title;
        document.getElementById('editUrl').value = url;
        document.getElementById('editCategory').value = categoryId;
        document.getElementById('editName').value = name || '';
        document.getElementById('editEmail').value = email || '';
        document.getElementById('editPhone').value = phone || '';
        document.getElementById('editModal').style.display = 'flex';
    }

    document.querySelectorAll('.edit-resource-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            openEditModal(this);
        });
    });

    resourceBoxes.forEach(wrapper => {
        wrapper.addEventListener('click', function () {
            openResourceInfoModal(this);
        });
        wrapper.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openResourceInfoModal(this);
            }
        });
    });

    window.onclick = function(event) {
        const editModal = document.getElementById('editModal');
        if (event.target == editModal) {
            editModal.style.display = 'none';
        }

        const infoModal = document.getElementById('resourceInfoModal');
        if (event.target == infoModal) {
            closeResourceInfoModal();
        }
    };

    // Filter resources on page after every letter added / removed
    searchInput.addEventListener("keyup", filterResources);

    // When the category dropdown changes, go to new pge
    categorySelect.addEventListener("change", (event) => {
        var selectedUrl = "/resources/search?category=" + event.target.value;
        window.location.href = selectedUrl;
    });
});
