document.addEventListener('DOMContentLoaded', function () {
    function showLoading() {
        document.getElementById('audit-table-body').innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-4">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <div class="mt-2">Loading...</div>
                    </td>
                </tr>
            `;
    }

    document.addEventListener('click', function (e) {
        if (e.target.closest('#audit-pagination a[data-page]')) {
            e.preventDefault();
            const pageNum = e.target.closest('a').dataset.page;
            loadPage(pageNum);
        }
    });

    function loadPage(page) {
        showLoading();

        fetch(`?page=${page}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');


                const newTableBody = doc.querySelector('#audit-table-body');
                if (newTableBody) {
                    document.getElementById('audit-table-body').innerHTML = newTableBody.innerHTML;
                }


                const newPagination = doc.querySelector('#audit-pagination');
                if (newPagination) {
                    document.getElementById('audit-pagination').innerHTML = newPagination.innerHTML;
                }


                const newShowingInfo = doc.querySelector('.card-header small');
                const currentShowingInfo = document.querySelector('.card-header small');
                if (newShowingInfo && currentShowingInfo) {
                    currentShowingInfo.textContent = newShowingInfo.textContent;
                }
            })
            .catch(error => {
                console.error('Error loading page:', error);
                document.getElementById('audit-table-body').innerHTML = `
                    <tr>
                        <td colspan="7" class="text-center py-4 text-danger">
                            <i class="bi bi-exclamation-triangle"></i>
                            Error loading data. Please try again.
                        </td>
                    </tr>
                `;
            });
    }
});