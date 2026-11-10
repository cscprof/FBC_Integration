// Toggle password visibility using Font Awesome icons.
document.querySelectorAll('.password-toggle').forEach(function (toggle) {
    const password = toggle.parentElement.querySelector('input');
    const icon = toggle.querySelector('i');

    toggle.addEventListener('click', function () {
        const visible = password.type === 'password';
        password.type = visible ? 'text' : 'password';
        icon.classList.toggle('fa-eye', visible);
        icon.classList.toggle('fa-eye-slash', !visible);
        toggle.setAttribute('aria-label', visible ? 'Hide password' : 'Show password');
        toggle.setAttribute('aria-pressed', String(visible));
    });
});
