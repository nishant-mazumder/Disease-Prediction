// Main JavaScript for MedPredict

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    initializeFormValidation();
    
    // Smooth scrolling for anchor links
    initializeSmoothScrolling();
    
    // Loading states for forms
    initializeLoadingStates();
    
    // Auto-hide alerts
    initializeAutoHideAlerts();
    
    // Prediction form enhancements
    initializePredictionForms();
});

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Smooth Scrolling
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Loading States
function initializeLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading me-2"></span>Processing...';
                submitBtn.disabled = true;
                
                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
}

// Auto-hide Alerts
function initializeAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Prediction Form Enhancements
function initializePredictionForms() {
    // Add input validation for prediction forms
    const predictionForms = document.querySelectorAll('form[action*="predict"]');
    
    predictionForms.forEach(form => {
        const inputs = form.querySelectorAll('input[type="number"]');
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                validatePredictionInput(this);
            });
            
            input.addEventListener('blur', function() {
                validatePredictionInput(this);
            });
        });
    });
}

// Validate prediction input
function validatePredictionInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    if (isNaN(value)) {
        input.classList.remove('is-valid', 'is-invalid');
        return;
    }
    
    if (value < min || value > max) {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        showInputError(input, `Value must be between ${min} and ${max}`);
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        hideInputError(input);
    }
}

// Show input error
function showInputError(input, message) {
    hideInputError(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    input.parentNode.appendChild(errorDiv);
}

// Hide input error
function hideInputError(input) {
    const errorDiv = input.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Utility Functions
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Chart functions for prediction results
function createConfidenceChart(containerId, confidence) {
    const canvas = document.getElementById(containerId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 60;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw background circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.fillStyle = '#e9ecef';
    ctx.fill();
    
    // Draw progress arc
    const startAngle = -Math.PI / 2;
    const endAngle = startAngle + (2 * Math.PI * confidence / 100);
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
    ctx.lineWidth = 10;
    ctx.strokeStyle = confidence > 70 ? '#dc3545' : confidence > 40 ? '#ffc107' : '#198754';
    ctx.stroke();
    
    // Draw text
    ctx.fillStyle = '#333';
    ctx.font = 'bold 20px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`${confidence}%`, centerX, centerY + 7);
}

// Search functionality for doctor search
function initializeDoctorSearch() {
    const searchForm = document.getElementById('doctor-search-form');
    if (!searchForm) return;
    
    const inputs = searchForm.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        input.addEventListener('change', function() {
            // Auto-submit form when filters change
            setTimeout(() => {
                searchForm.submit();
            }, 500);
        });
    });
}

// Initialize doctor search if on doctor search page
if (window.location.pathname.includes('doctors')) {
    initializeDoctorSearch();
}

// Prediction form auto-save (localStorage)
function initializeAutoSave() {
    const predictionForms = document.querySelectorAll('form[action*="predict"]');
    
    predictionForms.forEach(form => {
        const formId = form.action.split('/').pop();
        const inputs = form.querySelectorAll('input');
        
        // Load saved data
        const savedData = localStorage.getItem(`prediction_${formId}`);
        if (savedData) {
            const data = JSON.parse(savedData);
            inputs.forEach(input => {
                if (data[input.name]) {
                    input.value = data[input.name];
                }
            });
        }
        
        // Save data on input change
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                const formData = {};
                inputs.forEach(inp => {
                    if (inp.value) {
                        formData[inp.name] = inp.value;
                    }
                });
                localStorage.setItem(`prediction_${formId}`, JSON.stringify(formData));
            });
        });
        
        // Clear saved data on successful submission
        form.addEventListener('submit', function() {
            localStorage.removeItem(`prediction_${formId}`);
        });
    });
}

// Initialize auto-save
initializeAutoSave();

// Responsive table handling
function initializeResponsiveTables() {
    const tables = document.querySelectorAll('.table-responsive table');
    
    tables.forEach(table => {
        if (table.offsetWidth > table.parentElement.offsetWidth) {
            table.parentElement.style.overflowX = 'auto';
        }
    });
}

// Initialize responsive tables
initializeResponsiveTables();

// Print functionality
function printPage() {
    window.print();
}

// Export prediction history
function exportPredictionHistory() {
    const table = document.querySelector('.table');
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td, th');
        const rowData = Array.from(cells).map(cell => cell.textContent.trim());
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'prediction_history.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="search" i]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            const modal = bootstrap.Modal.getInstance(openModal);
            if (modal) {
                modal.hide();
            }
        }
    }
});

// Performance monitoring
function initializePerformanceMonitoring() {
    // Monitor page load time
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        
        // Send to analytics if available
        if (typeof gtag !== 'undefined') {
            gtag('event', 'page_load_time', {
                'value': Math.round(loadTime)
            });
        }
    });
}

// Initialize performance monitoring
initializePerformanceMonitoring();
