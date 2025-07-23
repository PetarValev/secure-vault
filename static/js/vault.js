document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const passwordField = document.getElementById(targetId);
            const icon = this.querySelector('i');

            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.className = 'bi bi-eye-slash';
            } else {
                passwordField.type = 'password';
                icon.className = 'bi bi-eye';
            }
        });
    });


    document.querySelectorAll('.copy-password').forEach(button => {
        button.addEventListener('click', function () {
            const password = this.getAttribute('data-password');
            const title = this.getAttribute('data-title');

            navigator.clipboard.writeText(password).then(function () {
                const toastMessage = document.getElementById('toastMessage');
                toastMessage.textContent = `Password for ${title} copied to clipboard!`;

                const toast = new bootstrap.Toast(document.getElementById('copyToast'));
                toast.show();
            });
        });
    });
});