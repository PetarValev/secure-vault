function showToast(type, title, message) {
    const toast = document.getElementById('successToast');
    const toastHeader = toast.querySelector('.toast-header');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    toastHeader.className = `toast-header text-white ${type === 'success' ? 'bg-success' : 'bg-danger'}`;
    const icon = toastHeader.querySelector('i');
    icon.className = type === 'success' ? 'bi bi-check-circle-fill me-2' : 'bi bi-exclamation-triangle-fill me-2';
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

document.getElementById('changePasswordBtn').addEventListener('click', function () {
    const button = this; // Запазваме референцията към бутона
    const oldPassword = document.getElementById('oldPassword').value;
    const newPassword1 = document.getElementById('newPassword1').value;
    const newPassword2 = document.getElementById('newPassword2').value;
    const errorDiv = document.getElementById('passwordErrors');

    errorDiv.classList.add('d-none');

    if (!oldPassword || !newPassword1 || !newPassword2) {
        errorDiv.textContent = 'All fields are required';
        errorDiv.classList.remove('d-none');
        return;
    }

    if (newPassword1 !== newPassword2) {
        errorDiv.textContent = 'New passwords do not match';
        errorDiv.classList.remove('d-none');
        return;
    }

    if (newPassword1.length < 8) {
        errorDiv.textContent = 'Password must be at least 8 characters long';
        errorDiv.classList.remove('d-none');
        return;
    }

    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Updating...';

    fetch(window.APP_URLS.changePassword, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            old_password: oldPassword,
            new_password1: newPassword1,
            new_password2: newPassword2
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            bootstrap.Modal.getInstance(document.getElementById('changePasswordModal')).hide();
            document.getElementById('changePasswordForm').reset();
            showToast('success', 'Password Changed', 'Your password has been updated successfully!');
        } else {
            errorDiv.textContent = data.error || 'Failed to change password';
            errorDiv.classList.remove('d-none');
        }
        button.disabled = false;
        button.innerHTML = '<i class="bi bi-key me-1"></i>Update Password';
    })
    .catch(error => {
        errorDiv.textContent = 'Something went wrong. Please try again.';
        errorDiv.classList.remove('d-none');
        button.disabled = false;
        button.innerHTML = '<i class="bi bi-key me-1"></i>Update Password';
    });
});

document.getElementById('confirmDeleteBtn').addEventListener('click', function () {
    const button = this; // Запазваме референцията към бутона
    const password = document.getElementById('deletePassword').value;
    const errorDiv = document.getElementById('passwordError');

    if (!password) {
        errorDiv.textContent = 'Password is required';
        errorDiv.classList.remove('d-none');
        return;
    }

    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Deleting...';

    fetch(window.APP_URLS.profileDelete, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            bootstrap.Modal.getInstance(document.getElementById('deleteAccountModal')).hide();
            showToast('success', 'Account Deleted', data.message);
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } else {
            errorDiv.textContent = data.error;
            errorDiv.classList.remove('d-none');
            button.disabled = false;
            button.innerHTML = '<i class="bi bi-trash me-1"></i>Delete My Account';
        }
    })
    .catch(error => {
        errorDiv.textContent = 'Something went wrong. Please try again.';
        errorDiv.classList.remove('d-none');
        button.disabled = false;
        button.innerHTML = '<i class="bi bi-trash me-1"></i>Delete My Account';
    });
});