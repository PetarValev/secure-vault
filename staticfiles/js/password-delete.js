document.addEventListener('DOMContentLoaded', function () {
    const confirmCheckbox = document.getElementById('confirmDelete');
    const deleteBtn = document.getElementById('deleteBtn');
    const deleteForm = document.getElementById('deleteForm');
    const finalDeleteBtn = document.getElementById('finalDeleteBtn');


    confirmCheckbox.addEventListener('change', function () {
        deleteBtn.disabled = !this.checked;
    });


    deleteForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const modal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
        modal.show();
    });


    finalDeleteBtn.addEventListener('click', function () {

        this.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Deleting...';
        this.disabled = true;


        deleteForm.submit();
    });


    let clickCount = 0;
    deleteBtn.addEventListener('click', function () {
        clickCount++;
        if (clickCount === 1) {
            this.innerHTML = '<i class="bi bi-exclamation-triangle me-1"></i>Are You Sure?';
            this.className = 'btn btn-outline-danger';

            setTimeout(() => {
                if (clickCount === 1) {
                    this.innerHTML = '<i class="bi bi-trash me-1"></i>Delete Permanently';
                    this.className = 'btn btn-danger';
                    clickCount = 0;
                }
            }, 3000);
        }
    });

});