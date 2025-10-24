// Account Form Enhancements
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.account-form');
    const inputs = form.querySelectorAll('input, select, textarea');
    
    // Real-time validation feedback
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.style.borderColor = '#f87171';
            } else {
                this.style.borderColor = '#3b82f6';
            }
        });
        
        input.addEventListener('focus', function() {
            this.style.borderColor = '#3b82f6';
        });
    });
    
    // Form submission feedback
    form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('.btn-primary');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.innerHTML = '<span class="btn-icon">⏳</span>Saving...';
        submitBtn.disabled = true;
        
        // Re-enable after 3 seconds (or handle via backend response)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 3000);
    });
    
    // Auto-format currency fields (if balance field exists)
    const balanceField = form.querySelector('input[name="balance"]');
    if (balanceField) {
        balanceField.addEventListener('input', function() {
            let value = this.value.replace(/[^0-9.]/g, '');
            if (value) {
                let parts = value.split('.');
                if (parts[1] && parts[1].length > 2) {
                    parts[1] = parts[1].substring(0, 2);
                }
                value = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',') + 
                       (parts[1] ? '.' + parts[1] : '');
                this.value = '$' + value;
            }
        });
    }
});
