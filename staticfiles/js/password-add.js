document.addEventListener('DOMContentLoaded', function () {
    const passwordField = document.querySelector('input[name="password"]');

    if (passwordField) {
        passwordField.addEventListener('input', function () {
            const password = this.value;
            const progressBar = document.getElementById('passwordStrength');
            const strengthLevel = document.getElementById('strengthLevel');

            if (password.length === 0) {
                progressBar.style.width = '0%';
                strengthLevel.textContent = '-';
                return;
            }

            let score = 0;
            if (password.length >= 8) score += 25;
            if (password.length >= 12) score += 25;
            if (/[a-z]/.test(password)) score += 15;
            if (/[A-Z]/.test(password)) score += 15;
            if (/[0-9]/.test(password)) score += 10;
            if (/[!@#$%^&*]/.test(password)) score += 10;

            if (score >= 80) {
                progressBar.style.width = '100%';
                progressBar.className = 'progress-bar bg-success';
                strengthLevel.textContent = 'Strong';
            } else if (score >= 60) {
                progressBar.style.width = score + '%';
                progressBar.className = 'progress-bar bg-warning';
                strengthLevel.textContent = 'Good';
            } else if (score >= 40) {
                progressBar.style.width = score + '%';
                progressBar.className = 'progress-bar bg-info';
                strengthLevel.textContent = 'Fair';
            } else {
                progressBar.style.width = score + '%';
                progressBar.className = 'progress-bar bg-danger';
                strengthLevel.textContent = 'Weak';
            }
        });
    }
});