document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    
    // Select all the input fields including the file input
    const fields = {
        firstName: form.querySelector('input[name="first_name"]'),
        lastName: form.querySelector('input[name="last_name"]'),
        phoneNumber: form.querySelector('input[name="phone_number"]'),
        dob: form.querySelector('input[name="dob"]'),
        gender: form.querySelector('select[name="gender"]'),
        email: form.querySelector('input[name="email"]'),
        password: form.querySelector('input[name="password"]'),
        confirmPassword: form.querySelector('input[name="confirm_password"]'),
        profilePicture: form.querySelector('input[name="profile_picture"]')
    };

    Object.values(fields).forEach(field => {
        if (field.type === 'file') {
            field.addEventListener('change', () => validateFile(field));
        } else {
            field.addEventListener('input', () => validateField(field));
        }
    });

    form.addEventListener('submit', (event) => {
        let valid = true;

        Object.values(fields).forEach(field => {
            if (!validateField(field)) {
                valid = false;
            }
        });

        // Validate file input separately
        if (!validateFile(fields.profilePicture)) {
            valid = false;
        }

        if (!valid) {
            event.preventDefault();
        }
    });

    function validateField(field) {
        let valid = true;
        clearErrors(field);

        switch (field.name) {
            case 'first_name':
            case 'last_name':
                if (!/^[A-Z][a-zA-Z]*$/.test(field.value)) {
                    showError(field, 'Must start with a capital letter and only letters.');
                    valid = false;
                }
                break;
            case 'phone_number':
                if (!/^\d{10}$/.test(field.value)) {
                    showError(field, 'Phone number should be 10 digits.');
                    valid = false;
                }
                break;
            case 'dob':
                if (!field.value) {
                    showError(field, 'Date of Birth is required.');
                    valid = false;
                }
                break;
            case 'gender':
                if (!field.value) {
                    showError(field, 'Gender is required.');
                    valid = false;
                }
                break;
            case 'email':
                if (!/^[\w.-]+@gmail\.com$/.test(field.value)) {
                    showError(field, 'Please enter a valid Gmail address.');
                    valid = false;
                }
                break;
            case 'password':
                if (!/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{5,}$/.test(field.value)) {
                    showError(field, 'Password must be at least 5 characters long, including special characters, letters, and numbers.');
                    valid = false;
                }
                break;
            case 'confirm_password':
                if (field.value !== fields.password.value) {
                    showError(field, 'Passwords do not match.');
                    valid = false;
                }
                break;
        }

        return valid;
    }

    function validateFile(field) {
        const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
        const file = field.files[0]; // Get the selected file
        let valid = true;

        // Clear previous error message
        clearErrors(field);

        if (file) {
            const fileName = file.name;

            if (!allowedExtensions.test(fileName)) {
                showError(field, 'Only .png, .jpg, and .jpeg file formats are allowed.');
                valid = false;
                field.value = ''; // Clear the file input
            }
        }

        return valid;
    }

    function showError(field, message) {
        // Create or update error message element
        let error = field.nextElementSibling;
        if (!error || !error.classList.contains('error-message')) {
            error = document.createElement('div');
            error.className = 'error-message';
            field.parentElement.insertBefore(error, field.nextSibling);
        }
        error.textContent = message;
    }

    function clearErrors(field) {
        let error = field.nextElementSibling;
        if (error && error.classList.contains('error-message')) {
            error.textContent = '';
        }
    }
});
