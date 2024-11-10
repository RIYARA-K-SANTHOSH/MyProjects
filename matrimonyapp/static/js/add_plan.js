document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('planForm');

    // Attach event listeners to all input elements
    form.querySelectorAll('input, textarea, select').forEach(element => {
        element.addEventListener('input', validateField); // For real-time validation
        element.addEventListener('change', validateField); // For select elements
    });

    function validateField(event) {
        const field = event.target;
        const errorMessage = document.getElementById(`${field.id}_error`);

        // Perform validation based on field type
        switch (field.id) {
            case 'plan_name':
                if (field.value.trim() === '') {
                    showError(errorMessage, 'Please select a plan name.');
                } else {
                    hideError(errorMessage);
                }
                break;
            case 'plan_details':
                if (field.value.trim() === '') {
                    showError(errorMessage, 'Please enter the plan details.');
                } else {
                    hideError(errorMessage);
                }
                break;
            case 'price':
                const priceValue = parseFloat(field.value);
                if (isNaN(priceValue) || priceValue <= 1000 || priceValue >= 50000) {
                    showError(errorMessage, 'Price must be between 1000 and 50000.');
                } else {
                    hideError(errorMessage);
                }
                break;
            case 'duration_months':
                const durationValue = parseInt(field.value, 10);
                if (isNaN(durationValue) || durationValue <= 0 || durationValue >= 13) {
                    showError(errorMessage, 'Duration must be between 1 and 12 months.');
                } else {
                    hideError(errorMessage);
                }
                break;
            default:
                break;
        }
    }

    function showError(errorMessageElement, message) {
        errorMessageElement.textContent = message;
        errorMessageElement.classList.add('show');
    }

    function hideError(errorMessageElement) {
        errorMessageElement.textContent = '';
        errorMessageElement.classList.remove('show');
    }
});
