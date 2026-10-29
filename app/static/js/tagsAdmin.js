function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('is-active');
        const firstInput = modal.querySelector('input:not([type="hidden"])');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 50);
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('is-active');
    }
}

function handleBackdropClick(event, modalId) {
    if (event.target === event.currentTarget) {
        closeModal(modalId);
    }
}

function openEditModal(tagId, tagName, tagType) {
    const form = document.getElementById('editTagForm');
    form.action = '/admin/tags/' + encodeURIComponent(tagId) + '/edit';
    document.getElementById('editTagName').value = tagName;
    document.getElementById('editTagType').value = tagType || '';
    openModal('editTagModal');
}

// Close modals on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal('newTagModal');
        closeModal('editTagModal');
    }
});

// Client-side search filtering
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('tagSearchInput');
    const tagItems = document.querySelectorAll('.tag-item');
    const noSearchMatchMessage = document.getElementById('noSearchMatchMessage');
    const tagCountText = document.getElementById('tagCountText');
    const totalTags = tagItems.length;

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.trim().toLowerCase();
            let visibleCount = 0;

            tagItems.forEach(function(item) {
                const name = item.getAttribute('data-tag-name') || '';
                const type = item.getAttribute('data-tag-type') || '';
                if (name.includes(query) || type.includes(query)) {
                    item.style.display = 'flex';
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                }
            });

            if (visibleCount === 0 && query !== '') {
                noSearchMatchMessage.style.display = 'block';
            } else {
                noSearchMatchMessage.style.display = 'none';
            }

            if (query === '') {
                tagCountText.innerHTML = '<strong>' + totalTags + '</strong> ' + (totalTags === 1 ? 'tag' : 'tags');
            } else {
                tagCountText.innerHTML = '<strong>' + visibleCount + '</strong> of <strong>' + totalTags + '</strong> ' + (totalTags === 1 ? 'tag' : 'tags');
            }
        });
    }
});
