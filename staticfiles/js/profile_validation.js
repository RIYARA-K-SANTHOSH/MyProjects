document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');

    // Select relevant input fields
    const fields = {
        firstName: form.querySelector('input[name="first_name"]'),
        lastName: form.querySelector('input[name="last_name"]'),
        phoneNumber: form.querySelector('input[name="phone_number"]'),
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
                    showError(field, 'Must start with a capital letter and contain only letters.');
                    valid = false;
                }
                break;
            case 'phone_number':
                if (!/^\d{10}$/.test(field.value)) {
                    showError(field, 'Phone number should be exactly 10 digits.');
                    valid = false;
                }
                break;
        }

        return valid;
    }

    function validateFile(field) {
        const allowedExtensions = /(\.jpg|\.jpeg)$/i;
        const file = field.files[0];
        let valid = true;

        clearErrors(field);

        if (file) {
            const fileName = file.name;

            if (!allowedExtensions.test(fileName)) {
                showError(field, 'Only .jpg and .jpeg file formats are allowed.');
                valid = false;
                field.value = ''; // Clear the file input
            }
        }

        return valid;
    }

    function showError(field, message) {
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
