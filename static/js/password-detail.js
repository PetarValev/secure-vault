document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('togglePassword');
    const passwordField = document.getElementById('passwordField');
    const toggleIcon = document.getElementById('toggleIcon');

    if (toggleBtn && passwordField && toggleIcon) {
        toggleBtn.addEventListener('click', function () {
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                toggleIcon.className = 'bi bi-eye-slash';
            } else {
                passwordField.type = 'password';
                toggleIcon.className = 'bi bi-eye';
            }
        });
    }

    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function () {
            const textToCopy = this.getAttribute('data-copy');
            const label = this.getAttribute('data-label');

            navigator.clipboard.writeText(textToCopy).then(function () {
                const toastMessage = document.getElementById('toastMessage');
                toastMessage.textContent = `${label} copied to clipboard!`;

                const toast = new bootstrap.Toast(document.getElementById('copyToast'));
                toast.show();
            });
        });
    });
});