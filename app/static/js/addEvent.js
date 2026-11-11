document.addEventListener('DOMContentLoaded', function() {
    const tagSearch = document.getElementById('tagSearch');
    const tagDropdown = document.getElementById('tagDropdown');
    const tagOptions = document.querySelectorAll('.tag-option:not(#createTagOption)');
    const createTagOption = document.getElementById('createTagOption');
    const createTagName = document.getElementById('createTagName');
    const noTagsMessage = document.getElementById('noTagsMessage');
    const selectedTagsContainer = document.getElementById('selectedTagsContainer');
    const hiddenTagsInputs = document.getElementById('hiddenTagsInputs');

    const selectedTags = new Set();
    const selectedNewTags = new Set();

    tagSearch.addEventListener('input', function() {
        const rawQuery = this.value;
        const query = rawQuery.trim().toLowerCase();
        let hasVisible = false;

        if (query === '') {
            tagDropdown.style.display = 'none';
            createTagOption.style.display = 'none';
            noTagsMessage.style.display = 'none';
            return;
        }

        tagDropdown.style.display = 'block';

        let exactExistingMatch = false;

        tagOptions.forEach(function(option) {
            const name = option.getAttribute('data-tag-name');
            const id = option.getAttribute('data-tag-id');
            if (name === query) {
                exactExistingMatch = true;
            }

            if (name.includes(query) && !selectedTags.has(id)) {
                option.style.display = 'block';
                hasVisible = true;
            } else {
                option.style.display = 'none';
            }
        });

        const isAlreadySelectedNew = selectedNewTags.has(query);

        if (!exactExistingMatch && !isAlreadySelectedNew) {
            createTagName.textContent = rawQuery.trim();
            createTagOption.style.display = 'block';
        } else {
            createTagOption.style.display = 'none';
        }

        if (!hasVisible && createTagOption.style.display === 'none') {
            if (isAlreadySelectedNew || exactExistingMatch) {
                noTagsMessage.textContent = 'Tag already selected';
            } else {
                noTagsMessage.textContent = 'No tags found';
            }
            noTagsMessage.style.display = 'block';
        } else {
            noTagsMessage.style.display = 'none';
        }
    });

    tagSearch.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (createTagOption.style.display !== 'none') {
                createTagOption.click();
            } else {
                for (let i = 0; i < tagOptions.length; i++) {
                    if (tagOptions[i].style.display !== 'none') {
                        tagOptions[i].click();
                        break;
                    }
                }
            }
        }
    });

    document.addEventListener('click', function(e) {
        if (!tagSearch.contains(e.target) && !tagDropdown.contains(e.target)) {
            tagDropdown.style.display = 'none';
        }
    });

    tagSearch.addEventListener('focus', function() {
        if (this.value.trim() !== '') {
            const evt = new Event('input');
            this.dispatchEvent(evt);
        }
    });

    tagOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            const id = this.getAttribute('data-tag-id');
            const name = this.innerText.trim();

            if (!selectedTags.has(id)) {
                selectedTags.add(id);
                addTag(id, name);
            }

            tagSearch.value = '';
            tagDropdown.style.display = 'none';
        });
    });

    createTagOption.addEventListener('click', function() {
        const rawName = tagSearch.value.trim();
        if (!rawName) return;

        // Check if it matches an existing tag
        let existingOption = null;
        tagOptions.forEach(function(opt) {
            if (opt.getAttribute('data-tag-name') === rawName.toLowerCase()) {
                existingOption = opt;
            }
        });

        if (existingOption) {
            const id = existingOption.getAttribute('data-tag-id');
            const name = existingOption.innerText.trim();
            if (!selectedTags.has(id)) {
                selectedTags.add(id);
                addTag(id, name);
            }
        } else {
            const lowerName = rawName.toLowerCase();
            if (!selectedNewTags.has(lowerName)) {
                selectedNewTags.add(lowerName);
                addNewTag(rawName);
            }
        }

        tagSearch.value = '';
        tagDropdown.style.display = 'none';
    });

    function addTag(id, name) {
        const tagEl = document.createElement('div');
        tagEl.className = 'selected-tag-pill';
        
        const text = document.createElement('span');
        text.textContent = name;
        tagEl.appendChild(text);

        const removeBtn = document.createElement('span');
        removeBtn.innerHTML = '&times;';
        removeBtn.className = 'selected-tag-remove';
        removeBtn.addEventListener('click', function() {
            selectedTags.delete(id);
            tagEl.remove();
            const hiddenInput = document.getElementById('hidden_tag_' + id);
            if (hiddenInput) hiddenInput.remove();
        });
        tagEl.appendChild(removeBtn);

        selectedTagsContainer.appendChild(tagEl);

        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'event_tags';
        hiddenInput.value = id;
        hiddenInput.id = 'hidden_tag_' + id;
        hiddenTagsInputs.appendChild(hiddenInput);
    }

    function addNewTag(name) {
        const tagEl = document.createElement('div');
        tagEl.className = 'selected-tag-pill';
        
        const text = document.createElement('span');
        text.textContent = name;
        tagEl.appendChild(text);

        const removeBtn = document.createElement('span');
        removeBtn.innerHTML = '&times;';
        removeBtn.className = 'selected-tag-remove';
        
        const lowerName = name.toLowerCase();
        const tagInputId = 'hidden_new_tag_' + Math.random().toString(36).substring(2, 9);

        removeBtn.addEventListener('click', function() {
            selectedNewTags.delete(lowerName);
            tagEl.remove();
            const hiddenInput = document.getElementById(tagInputId);
            if (hiddenInput) hiddenInput.remove();
        });
        tagEl.appendChild(removeBtn);

        selectedTagsContainer.appendChild(tagEl);

        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'new_tags';
        hiddenInput.value = name;
        hiddenInput.id = tagInputId;
        hiddenTagsInputs.appendChild(hiddenInput);
    }
});
