document.addEventListener('DOMContentLoaded', function () {
    const runAuditBtn = document.getElementById('run-audit-btn');
    const runNewAuditBtn = document.getElementById('run-new-audit-btn');
    const emptyState = document.getElementById('empty-state');
    const loadingState = document.getElementById('loading-state');
    const resultsState = document.getElementById('results-state');
    const passwordAnalysisSection = document.getElementById('password-analysis-section');

    function runAudit() {
        // Hide other states and show loading
        emptyState.classList.add('d-none');
        resultsState.classList.add('d-none');
        loadingState.classList.remove('d-none');
        passwordAnalysisSection.classList.add('d-none');

        // Use window variables instead of Django template tags
        fetch(window.auditUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': window.csrfToken,
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displayResults(data.audit, data.password_analysis);
                    showToast(data.message);
                    updateAuditHistory(data.audit);
                } else {
                    showError(data.error || 'Audit failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('An error occurred while running the audit');
            });
    }

    function displayResults(audit, passwordAnalysis) {
        // Hide loading and show results
        loadingState.classList.add('d-none');
        resultsState.classList.remove('d-none');
        passwordAnalysisSection.classList.remove('d-none');

        // Update header color based on score
        const header = document.getElementById('results-header');
        const score = audit.security_score;
        if (score >= 80) {
            header.className = 'card-header bg-success text-white';
        } else if (score >= 60) {
            header.className = 'card-header bg-warning text-white';
        } else {
            header.className = 'card-header bg-danger text-white';
        }

        // Update basic stats
        document.getElementById('security-score').textContent = score;
        document.getElementById('audit-date').textContent = audit.created_at;
        document.getElementById('total-passwords').textContent = audit.total_passwords;

        // Update weak passwords with color
        const weakElement = document.getElementById('weak-passwords');
        weakElement.textContent = audit.weak_passwords;
        weakElement.className = audit.weak_passwords === 0 ? 'text-success fw-bold mb-1' : 'text-danger fw-bold mb-1';

        // Update duplicate passwords with color
        const duplicateElement = document.getElementById('duplicate-passwords');
        duplicateElement.textContent = audit.duplicate_passwords;
        duplicateElement.className = audit.duplicate_passwords === 0 ? 'text-success fw-bold mb-1' : 'text-warning fw-bold mb-1';

        // Update old passwords with color
        const oldElement = document.getElementById('old-passwords');
        oldElement.textContent = audit.old_passwords;
        oldElement.className = audit.old_passwords === 0 ? 'text-success fw-bold mb-1' : 'text-info fw-bold mb-1';

        // Update emoji based on score
        const emoji = document.getElementById('security-emoji');
        if (score >= 80) {
            emoji.className = 'bi bi-emoji-smile fs-1';
        } else if (score >= 60) {
            emoji.className = 'bi bi-emoji-neutral fs-1';
        } else {
            emoji.className = 'bi bi-emoji-frown fs-1';
        }

        // Update password analysis table
        updatePasswordAnalysisTable(passwordAnalysis);
    }

    function updatePasswordAnalysisTable(passwordAnalysis) {
        const tableBody = document.getElementById('password-analysis-table');
        tableBody.innerHTML = '';

        passwordAnalysis.forEach(analysis => {
            const row = document.createElement('tr');

            // Create strength badge
            let strengthBadge = '';
            const score = analysis.entry.strength_score;
            if (score >= 80) {
                strengthBadge = '<span class="badge bg-success">Strong</span>';
            } else if (score >= 60) {
                strengthBadge = '<span class="badge bg-warning">Good</span>';
            } else if (score >= 40) {
                strengthBadge = '<span class="badge bg-info">Fair</span>';
            } else {
                strengthBadge = '<span class="badge bg-danger">Weak</span>';
            }

            // Create issues badges
            let issuesHtml = '';
            if (analysis.issues.length > 0) {
                issuesHtml = analysis.issues.map(issue =>
                    `<span class="badge bg-warning text-dark me-1">${issue}</span>`
                ).join('');
            } else {
                issuesHtml = '<span class="text-success"><i class="bi bi-check-circle me-1"></i>No issues</span>';
            }

            // Calculate time ago
            const updatedAt = new Date(analysis.entry.updated_at);
            const now = new Date();
            const diffTime = Math.abs(now - updatedAt);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            const timeAgo = diffDays === 1 ? '1 day ago' : `${diffDays} days ago`;

            row.innerHTML = `
                <td>
                    <div class="d-flex align-items-center">
                        <i class="bi bi-key me-2 text-muted"></i>
                        <strong>${analysis.entry.title}</strong>
                    </div>
                </td>
                <td>${analysis.entry.username}</td>
                <td>${strengthBadge}</td>
                <td>${issuesHtml}</td>
                <td><small class="text-muted">${timeAgo}</small></td>
            `;

            tableBody.appendChild(row);
        });
    }

    function updateAuditHistory(audit) {
        const historyTable = document.getElementById('audit-history-table');
        if (historyTable) {
            // Add new row at the beginning
            const newRow = document.createElement('tr');

            let scoreBadgeClass = '';
            if (audit.security_score >= 80) {
                scoreBadgeClass = 'bg-success';
            } else if (audit.security_score >= 60) {
                scoreBadgeClass = 'bg-warning';
            } else {
                scoreBadgeClass = 'bg-danger';
            }

            newRow.innerHTML = `
                <td>Just now</td>
                <td>
                    <span class="badge ${scoreBadgeClass}">
                        ${audit.security_score}%
                    </span>
                </td>
                <td>${audit.total_passwords}</td>
                <td>${audit.weak_passwords}</td>
                <td>${audit.duplicate_passwords}</td>
                <td>${audit.old_passwords}</td>
            `;

            historyTable.insertBefore(newRow, historyTable.firstChild);

            // Keep only last 5 entries
            if (historyTable.children.length > 5) {
                historyTable.removeChild(historyTable.lastChild);
            }
        }
    }

    function showError(message) {
        loadingState.classList.add('d-none');
        emptyState.classList.remove('d-none');

        document.getElementById('auditToastMessage').textContent = message;
        document.querySelector('#auditToast .bi').className = 'bi bi-exclamation-triangle text-danger me-2';
        const toast = new bootstrap.Toast(document.getElementById('auditToast'));
        toast.show();
    }

    function showToast(message) {
        document.getElementById('auditToastMessage').textContent = message;
        document.querySelector('#auditToast .bi').className = 'bi bi-check-circle text-success me-2';
        const toast = new bootstrap.Toast(document.getElementById('auditToast'));
        toast.show();
    }

    // Event listeners
    if (runAuditBtn) {
        runAuditBtn.addEventListener('click', runAudit);
    }

    if (runNewAuditBtn) {
        runNewAuditBtn.addEventListener('click', runAudit);
    }
});