document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn1 = document.getElementById('togglePassword1');
    const toggleBtn2 = document.getElementById('togglePassword2');
    const passwordField1 = document.querySelector('input[name="password1"]');
    const passwordField2 = document.querySelector('input[name="password2"]');
    const toggleIcon1 = document.getElementById('toggleIcon1');
    const toggleIcon2 = document.getElementById('toggleIcon2');

    if (toggleBtn1 && passwordField1 && toggleIcon1) {
        toggleBtn1.addEventListener('click', function () {
            if (passwordField1.type === 'password') {
                passwordField1.type = 'text';
                toggleIcon1.className = 'bi bi-eye-slash';
            } else {
                passwordField1.type = 'password';
                toggleIcon1.className = 'bi bi-eye';
            }
        });
    }

    if (toggleBtn2 && passwordField2 && toggleIcon2) {
        toggleBtn2.addEventListener('click', function () {
            if (passwordField2.type === 'password') {
                passwordField2.type = 'text';
                toggleIcon2.className = 'bi bi-eye-slash';
            } else {
                passwordField2.type = 'password';
                toggleIcon2.className = 'bi bi-eye';
            }
        });
    }

    const progressBar = document.getElementById('passwordStrength');
    const strengthLevel = document.getElementById('strengthLevel');

    if (passwordField1 && progressBar && strengthLevel) {
        passwordField1.addEventListener('input', function () {
            const password = this.value;

            if (password.length === 0) {
                progressBar.style.width = '0%';
                strengthLevel.textContent = '';
                return;
            }

            let score = 0;

            if (password.length >= 8) score += 25;
            if (password.length >= 12) score += 25;

            if (/[a-z]/.test(password)) score += 15;
            if (/[A-Z]/.test(password)) score += 15;
            if (/[0-9]/.test(password)) score += 10;
            if (/[^A-Za-z0-9]/.test(password)) score += 10;

            progressBar.style.width = score + '%';

            if (score >= 80) {
                progressBar.className = 'progress-bar bg-success';
                strengthLevel.textContent = 'Strong';
                strengthLevel.className = 'text-success fw-medium';
            } else if (score >= 60) {
                progressBar.className = 'progress-bar bg-warning';
                strengthLevel.textContent = 'Good';
                strengthLevel.className = 'text-warning fw-medium';
            } else if (score >= 40) {
                progressBar.className = 'progress-bar bg-info';
                strengthLevel.textContent = 'Fair';
                strengthLevel.className = 'text-info fw-medium';
            } else {
                progressBar.className = 'progress-bar bg-danger';
                strengthLevel.textContent = 'Weak';
                strengthLevel.className = 'text-danger fw-medium';
            }
        });
    }
});
