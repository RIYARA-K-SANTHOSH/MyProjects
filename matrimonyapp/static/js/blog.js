document.addEventListener('DOMContentLoaded', function() {
    // Get input elements
    const titleInput = document.getElementById('id_title');
    const contentInput = document.getElementById('id_content');
    const imageInput = document.getElementById('id_image');

    // Add event listeners to each field for real-time validation
    titleInput.addEventListener('input', function() {
        validateTitle(titleInput.value);
    });

    contentInput.addEventListener('input', function() {
        validateContent(contentInput.value);
    });

    imageInput.addEventListener('change', function() {
        validateImage(imageInput.files[0]);
    });

    // Validate the title
    function validateTitle(title) {
        const titleRegex = /^[A-Z][a-zA-Z\s]*$/;
        const errorElement = document.getElementById('title-error');

        if (title.trim() === '') {
            errorElement.textContent = 'Title is required.';
            return false;
        }
        if (!titleRegex.test(title)) {
            errorElement.textContent = 'Title must start with a capital letter and contain only letters.';
            return false;
        }

        errorElement.textContent = ''; // Clear error if valid
        return true;
    }

    // Validate the content
    function validateContent(content) {
        const contentRegex = /^[A-Z][a-zA-Z\s]*$/;
        const errorElement = document.getElementById('content-error');

        if (content.trim() === '') {
            errorElement.textContent = 'Content is required.';
            return false;
        }
        if (!contentRegex.test(content)) {
            errorElement.textContent = 'Content must start with a capital letter and contain only letters.';
            return false;
        }

        errorElement.textContent = ''; // Clear error if valid
        return true;
    }

    // Validate the image
    function validateImage(imageFile) {
        const validImageTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        const errorElement = document.getElementById('image-error');

        if (imageFile && !validImageTypes.includes(imageFile.type)) {
            errorElement.textContent = 'Only JPEG, JPG, or PNG formats are supported for the image.';
            return false;
        }

        errorElement.textContent = ''; // Clear error if valid
        return true;
    }
});
