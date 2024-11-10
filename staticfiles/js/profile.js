function validateForm(event) {
    event.preventDefault();

    // Clear previous error messages
    const errorElements = document.querySelectorAll('.error-message');
    errorElements.forEach(el => el.textContent = '');

    // Get form values
    const address = document.getElementById('address').value.trim();
    const height = document.getElementById('height').value.trim();
    const weight = document.getElementById('weight').value.trim();
    const about = document.getElementById('about').value.trim();
    const age = document.getElementById('age').value.trim();
    const hobbies = document.getElementById('hobbies').value.trim();
    const occupation = document.getElementById('occupation').value.trim();
    const annualIncome = document.getElementById('annual_income').value.trim();

    let isValid = true;

    // Validate Address
    if (address === '') {
        document.getElementById('address-error').textContent = 'Address is required.';
        isValid = false;
    }

    // Validate Height
    if (height === '' || isNaN(height) || height <= 0) {
        document.getElementById('height-error').textContent = 'Height must be a positive number.';
        isValid = false;
    }

    // Validate Weight
    if (weight && (isNaN(weight) || weight < 0)) {
        document.getElementById('weight-error').textContent = 'Weight must be a non-negative number.';
        isValid = false;
    }

    // Validate About Me
    if (about === '') {
        document.getElementById('about-error').textContent = 'About Me is required.';
        isValid = false;
    }

    // Validate Age
    if (age && (isNaN(age) || age <= 0)) {
        document.getElementById('age-error').textContent = 'Age must be a positive number.';
        isValid = false;
    }

    // Validate Hobbies
    if (hobbies === '') {
        document.getElementById('hobbies-error').textContent = 'Hobbies are required.';
        isValid = false;
    }

    // Validate Occupation
    if (occupation === '') {
        document.getElementById('occupation-error').textContent = 'Occupation is required.';
        isValid = false;
    }

    // Validate Annual Income
    if (annualIncome && (isNaN(annualIncome) || annualIncome < 0)) {
        document.getElementById('annual-income-error').textContent = 'Annual income must be a non-negative number.';
        isValid = false;
    }

    // Submit form if valid
    if (isValid) {
        document.getElementById('profileForm').submit();
    }
}

// Function to clear error messages while typing
function clearError(event) {
    const inputId = event.target.id;
    const errorId = `${inputId}-error`;
    document.getElementById(errorId).textContent = '';
}

// Add event listeners for input fields to clear errors while typing
document.querySelectorAll('input, textarea').forEach(input => {
    input.addEventListener('input', clearError);
});
