document.addEventListener('DOMContentLoaded', function () {
    let passwordHistory = [];
    const lengthSlider = document.getElementById('length');
    const lengthValue = document.getElementById('lengthValue');
    const generateBtn = document.getElementById('generateBtn');
    const generatedPassword = document.getElementById('generatedPassword');
    const copyGenerated = document.getElementById('copyGenerated');
    const strengthBadge = document.getElementById('strengthBadge');
    const strengthBar = document.getElementById('strengthBar');
    const historyContainer = document.getElementById('passwordHistory');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');

    lengthSlider.addEventListener('input', function () {
        lengthValue.textContent = this.value;
    });

    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const length = this.dataset.length;
            const upper = this.dataset.upper === 'true';
            const lower = this.dataset.lower === 'true';
            const numbers = this.dataset.numbers === 'true';
            const symbols = this.dataset.symbols === 'true';

            lengthSlider.value = length;
            lengthValue.textContent = length;
            document.getElementById('include_uppercase').checked = upper;
            document.getElementById('include_lowercase').checked = lower;
            document.getElementById('include_numbers').checked = numbers;
            document.getElementById('include_symbols').checked = symbols;
        });
    });

    function generatePassword() {
        const length = parseInt(lengthSlider.value);
        const includeUpper = document.getElementById('include_uppercase').checked;
        const includeLower = document.getElementById('include_lowercase').checked;
        const includeNumbers = document.getElementById('include_numbers').checked;
        const includeSymbols = document.getElementById('include_symbols').checked;

        let chars = '';
        if (includeLower) chars += 'abcdefghijklmnopqrstuvwxyz';
        if (includeUpper) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        if (includeNumbers) chars += '0123456789';
        if (includeSymbols) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?';

        if (!chars) {
            showToast('error', 'Please select at least one character type!');
            return;
        }

        let password = '';
        for (let i = 0; i < length; i++) {
            password += chars.charAt(Math.floor(Math.random() * chars.length));
        }

        generatedPassword.value = password;
        updatePasswordStrength(password);
        addToHistory(password);
    }

    function updatePasswordStrength(password) {
        let score = 0;
        if (password.length >= 8) score += 25;
        if (password.length >= 12) score += 25;
        if (/[a-z]/.test(password)) score += 15;
        if (/[A-Z]/.test(password)) score += 15;
        if (/[0-9]/.test(password)) score += 10;
        if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) score += 10;

        strengthBar.style.width = score + '%';

        if (score >= 80) {
            strengthBar.className = 'progress-bar bg-success';
            strengthBadge.className = 'badge bg-success';
            strengthBadge.textContent = 'Strong';
        } else if (score >= 60) {
            strengthBar.className = 'progress-bar bg-warning';
            strengthBadge.className = 'badge bg-warning text-dark';
            strengthBadge.textContent = 'Good';
        } else if (score >= 40) {
            strengthBar.className = 'progress-bar bg-info';
            strengthBadge.className = 'badge bg-info';
            strengthBadge.textContent = 'Fair';
        } else {
            strengthBar.className = 'progress-bar bg-danger';
            strengthBadge.className = 'badge bg-danger';
            strengthBadge.textContent = 'Weak';
        }
    }

    function addToHistory(password) {
        const timestamp = new Date().toLocaleTimeString();
        passwordHistory.unshift({password, timestamp});
        if (passwordHistory.length > 5) {
            passwordHistory = passwordHistory.slice(0, 5);
        }
        updateHistoryDisplay();
        clearHistoryBtn.disabled = false;
    }

    function updateHistoryDisplay() {
        if (passwordHistory.length === 0) {
            historyContainer.innerHTML = `
                <div class="text-center text-muted py-3">
                    <i class="bi bi-clock-history fs-4 d-block mb-2"></i>
                    <small>Generated passwords will appear here</small>
                </div>
            `;
            return;
        }

        historyContainer.innerHTML = passwordHistory.map((item, index) => `
            <div class="d-flex align-items-center justify-content-between p-2 ${index > 0 ? 'border-top' : ''}">
                <div class="flex-grow-1 me-2">
                    <input type="text" class="form-control form-control-sm font-monospace"
                           value="${item.password}" readonly>
                </div>
                <div class="d-flex gap-1">
                    <small class="text-muted me-2">${item.timestamp}</small>
                    <button class="btn btn-sm btn-outline-primary copy-history-password"
                            data-password="${item.password}">
                        <i class="bi bi-clipboard"></i>
                    </button>
                </div>
            </div>
        `).join('');

        document.querySelectorAll('.copy-history-password').forEach(btn => {
            btn.addEventListener('click', function () {
                const password = this.dataset.password;
                navigator.clipboard.writeText(password).then(() => {
                    showToast('success', 'Password copied to clipboard!');
                });
            });
        });
    }

    generateBtn.addEventListener('click', generatePassword);

    copyGenerated.addEventListener('click', function () {
        if (generatedPassword.value) {
            navigator.clipboard.writeText(generatedPassword.value).then(() => {
                showToast('success', 'Password copied to clipboard!');
            });
        }
    });

    clearHistoryBtn.addEventListener('click', function () {
        passwordHistory = [];
        updateHistoryDisplay();
        clearHistoryBtn.disabled = true;
    });
});