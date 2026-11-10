// Search function
(function () {
  const search = document.getElementById('globalSearch');
  const clearBtn = document.getElementById('clearBtn');
  const resultCount = document.getElementById('resultCount');
  const noResults = document.getElementById('noResults');
  const cards = document.querySelectorAll('.user-card');

  if (!search || !cards.length) return;

  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  //Highlights text from search function and on matching user cards
  function highlightText(el, term) {
    const original = el.dataset.original || el.textContent;
    el.dataset.original = original;

    if (!term) {
      el.innerHTML = escapeHtml(original);
      return;
    }

    const lower = original.toLowerCase();
    const idx = lower.indexOf(term);
    if (idx === -1) {
      el.innerHTML = escapeHtml(original);
      return;
    }

    el.innerHTML =
      escapeHtml(original.slice(0, idx)) +
      '<span class="highlight">' + escapeHtml(original.slice(idx, idx + term.length)) + '</span>' +
      escapeHtml(original.slice(idx + term.length));
  }

  //applies search filter and hides cards that do not fit criteria
  function applyFilter() {
    const term = search.value.trim().toLowerCase();
    let visible = 0;

    cards.forEach(card => {
      const haystack = card.dataset.search || '';
      const show = !term || haystack.includes(term);
      card.classList.toggle('hidden', !show);

      card.querySelectorAll('.searchable-text').forEach(el => highlightText(el, term));
      if (show) visible++;
    });

    resultCount.textContent = `${visible} / ${cards.length} users`;
    noResults.style.display = visible === 0 ? 'block' : 'none';
  }

  search.addEventListener('input', applyFilter);

// Clears search function
  clearBtn.addEventListener('click', () => {
    search.value = '';
    applyFilter();
    search.focus();
  });

  applyFilter();
})();
