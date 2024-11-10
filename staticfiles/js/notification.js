document.addEventListener('DOMContentLoaded', function() {
    // Get input elements
    const titleInput = document.getElementById('title');
    const messageInput = document.getElementById('message');
    
    // Add event listeners to each field for real-time validation
    titleInput.addEventListener('input', function() {
        validateTitle(titleInput.value);
    });

    messageInput.addEventListener('input', function() {
        validateMessage(messageInput.value);
    });

    // Validate the title
    function validateTitle(title) {
        const titleRegex = /^[A-Z][a-zA-Z\s]*$/;
        const errorElement = document.getElementById('title-error');

        if (!title) {
            errorElement.textContent = 'Title is required.';
        } else if (!titleRegex.test(title)) {
            errorElement.textContent = 'Title must start with a capital letter and contain only letters.';
        } else {
            errorElement.textContent = ''; // Clear error if valid
        }
    }

    // Validate the message
    function validateMessage(message) {
        const messageRegex = /^[A-Z][a-zA-Z0-9\s!@#$%^&*()_+.,?]*$/; // Starts with a capital letter, can contain letters, numbers, and special characters
        const errorElement = document.getElementById('message-error');

        if (!message) {
            errorElement.textContent = 'Message is required.';
        } else if (!messageRegex.test(message)) {
            errorElement.textContent = 'Message must start with a capital letter and can include letters, numbers, and special characters.';
        } else {
            errorElement.textContent = ''; // Clear error if valid
        }
    }
});
