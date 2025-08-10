function showToast(type, titleOrMessage, message) {
    let actualTitle, actualMessage;
    if (message === undefined) {
        actualMessage = titleOrMessage;
        actualTitle = null;
    } else {
        actualTitle = titleOrMessage;
        actualMessage = message;
    }

    let toast = document.getElementById('successToast');
    if (!toast) {
        const toastHTML = `
            <div class="toast-container position-fixed top-0 end-0 p-3">
                <div id="successToast" class="toast" role="alert">
                    <div class="toast-header text-white">
                        <i class="bi bi-check-circle-fill me-2"></i>
                        <strong class="me-auto" id="toastTitle">Notification</strong>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
                    </div>
                    <div class="toast-body" id="toastMessage">Message</div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', toastHTML);
        toast = document.getElementById('successToast');
    }

    const toastHeader = toast.querySelector('.toast-header');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessageElement = document.getElementById('toastMessage');

    let bgClass, iconClass, defaultTitle;
    switch(type) {
        case 'success':
            bgClass = 'bg-success';
            iconClass = 'bi bi-check-circle-fill me-2';
            defaultTitle = 'Success!';
            break;
        case 'error':
        case 'danger':
            bgClass = 'bg-danger';
            iconClass = 'bi bi-exclamation-triangle-fill me-2';
            defaultTitle = 'Error!';
            break;
        case 'warning':
            bgClass = 'bg-warning';
            iconClass = 'bi bi-exclamation-triangle-fill me-2';
            defaultTitle = 'Warning!';
            break;
        case 'info':
            bgClass = 'bg-info';
            iconClass = 'bi bi-info-circle-fill me-2';
            defaultTitle = 'Info';
            break;
        default:
            bgClass = 'bg-secondary';
            iconClass = 'bi bi-bell-fill me-2';
            defaultTitle = 'Notification';
    }

    toastHeader.className = `toast-header text-white ${bgClass}`;
    const icon = toastHeader.querySelector('i');
    icon.className = iconClass;

    toastTitle.textContent = actualTitle || defaultTitle;
    toastMessageElement.textContent = actualMessage;

    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 2000
    });

    toast.setAttribute('data-bs-autohide', 'true');
    toast.setAttribute('data-bs-delay', '2000');
    bsToast.show();
}