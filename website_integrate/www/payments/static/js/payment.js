document.addEventListener('DOMContentLoaded', () => {
    const paymentForm = document.getElementById('paymentForm');
    const submitButton = document.getElementById('submitPayment');
    const statusMessage = document.getElementById('statusMessage');

    paymentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Disable form while processing
        submitButton.disabled = true;
        submitButton.classList.add('loading');
        submitButton.textContent = 'Processing...';
        
        const formData = {
            amount: document.getElementById('amount').value,
            currency: document.getElementById('currency').value,
            reference: generateReference(),
        };

        try {
            const response = await fetch('/initiate-payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                showMessage('Payment initiated successfully! Redirecting...', 'success');
                // Here you would typically redirect to Relworx's payment page
                // window.location.href = data.payment_url;
            } else {
                throw new Error(data.error || 'Payment initiation failed');
            }
        } catch (error) {
            showMessage(error.message, 'error');
        } finally {
            submitButton.disabled = false;
            submitButton.classList.remove('loading');
            submitButton.textContent = 'Pay Now';
        }
    });

    function generateReference() {
        return 'REF-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    }

    function showMessage(message, type) {
        statusMessage.textContent = message;
        statusMessage.className = 'status-message ' + type;
    }
}); 