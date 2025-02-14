document.addEventListener('DOMContentLoaded', () => {
    const paymentForm = document.getElementById('paymentForm');
    const submitButton = document.getElementById('submitPayment');
    const statusMessage = document.getElementById('statusMessage');
    const amountInput = document.getElementById('amount');
    const phoneInput = document.getElementById('phone');

    // Format amount with commas for display
    function formatAmount(amount) {
        return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    // Format phone number to international format
    function formatPhoneNumber(phone) {
        const cleaned = phone.replace(/\D/g, '');
        return cleaned.startsWith('256') ? `+${cleaned}` : `+256${cleaned.substring(1)}`;
    }

    // Generate unique reference (8-36 characters)
    function generateReference() {
        const timestamp = Date.now().toString(36);
        const random = Math.random().toString(36).substring(2, 6);
        return `REL${timestamp}${random}`.toUpperCase();
    }

    // Validate phone number format
    phoneInput.addEventListener('input', (e) => {
        const value = e.target.value.replace(/[^\d]/g, '');
        e.target.value = value;
        
        if (value.length === 10) {
            validatePhoneNumber(value);
        } else {
            e.target.setCustomValidity('Phone number must be 10 digits');
        }
    });

    // Validate phone number with API
    async function validatePhoneNumber(phone) {
        try {
            const response = await fetch('/api/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    msisdn: formatPhoneNumber(phone)
                })
            });

            const data = await response.json();
            if (data.success) {
                phoneInput.setCustomValidity('');
                showMessage(`Validated: ${data.customer_name}`, 'success');
            } else {
                phoneInput.setCustomValidity('Invalid mobile money number');
                showMessage('Invalid mobile money number', 'error');
            }
        } catch (error) {
            console.error('Phone validation error:', error);
        }
    }

    // Format amount on input
    amountInput.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        if (value < 1000) {
            e.target.setCustomValidity('Amount must be at least UGX 1,000');
        } else {
            e.target.setCustomValidity('');
        }
    });

    // Handle form submission
    paymentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Disable form while processing
        submitButton.disabled = true;
        submitButton.classList.add('loading');
        submitButton.textContent = 'Processing...';
        
        const formData = {
            account_no: RELWORX_CONFIG.ACCOUNT_NO,
            reference: generateReference(),
            msisdn: formatPhoneNumber(phoneInput.value),
            currency: 'UGX',
            amount: parseFloat(amountInput.value),
            description: document.getElementById('description').value || 'Payment Request'
        };

        try {
            const response = await fetch('/api/payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                showMessage(`${data.message} Reference: ${formData.reference}`, 'success');
                // Store reference for tracking
                localStorage.setItem('paymentReference', formData.reference);
                localStorage.setItem('internalReference', data.internal_reference);
                
                // Reset form
                paymentForm.reset();
            } else {
                throw new Error(data.message || 'Payment request failed. Please try again.');
            }
        } catch (error) {
            showMessage(error.message, 'error');
        } finally {
            submitButton.disabled = false;
            submitButton.classList.remove('loading');
            submitButton.textContent = 'Pay Now';
        }
    });

    function showMessage(message, type) {
        statusMessage.textContent = message;
        statusMessage.className = 'status-message ' + type;
    }
}); 