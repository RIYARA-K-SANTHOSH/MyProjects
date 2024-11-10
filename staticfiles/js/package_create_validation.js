document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const nameInput = document.getElementById('name');
    const priceInput = document.getElementById('price');
    const descriptionInput = document.getElementById('description');
    const durationInput = document.getElementById('duration_days');

    function showError(input, message) {
        const errorElement = input.nextElementSibling;
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    function hideError(input) {
        const errorElement = input.nextElementSibling;
        errorElement.style.display = 'none';
    }

    function validateName() {
        if (!/^[A-Za-z\s]+$/.test(nameInput.value.trim())) {
            showError(nameInput, 'Name should contain only letters and spaces.');
            return false;
        }
        hideError(nameInput);
        return true;
    }

    function validatePrice() {
        if (!/^\d+(\.\d{1,2})?$/.test(priceInput.value) || parseFloat(priceInput.value) <= 0) {
            showError(priceInput, 'Price should be a positive number with up to 2 decimal places.');
            return false;
        }
        hideError(priceInput);
        return true;
    }

    function validateDescription() {
        if (!/^[A-Za-z0-9\s.,!?()-]+$/.test(descriptionInput.value.trim())) {
            showError(descriptionInput, 'Description should contain only letters, numbers, and basic punctuation.');
            return false;
        }
        hideError(descriptionInput);
        return true;
    }

    function validateDuration() {
        if (!/^\d+$/.test(durationInput.value) || parseInt(durationInput.value) <= 0) {
            showError(durationInput, 'Duration should be a positive integer.');
            return false;
        }
        hideError(durationInput);
        return true;
    }

    nameInput.addEventListener('input', validateName);
    priceInput.addEventListener('input', validatePrice);
    descriptionInput.addEventListener('input', validateDescription);
    durationInput.addEventListener('input', validateDuration);

    form.addEventListener('submit', function(event) {
        let isValid = validateName() & validatePrice() & validateDescription() & validateDuration();
        
        if (!isValid) {
            event.preventDefault();
        }
    });
});