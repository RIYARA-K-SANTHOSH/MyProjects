document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('messages');
    const messageInput = document.getElementById('messageInput');
    const sendMessageButton = document.getElementById('sendMessage');
    const recipientId = '{{ recipient.user_id }}';  // Get the recipient ID from the context

    function fetchMessages() {
        fetch(`/get-messages/${recipientId}/`)
            .then(response => response.json())
            .then(data => {
                messagesContainer.innerHTML = ''; // Clear previous messages
                data.messages.forEach(message => {
                    const messageElement = document.createElement('p');
                    messageElement.textContent = `${message.sender}: ${message.content}`;
                    messagesContainer.appendChild(messageElement);
                });
                messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll to bottom
            });
    }

    sendMessageButton.addEventListener('click', function() {
        const messageText = messageInput.value.trim();
        if (messageText) {
            const messageData = {
                content: messageText,
                recipient_id: recipientId
            };

            fetch('/send-message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if required
                },
                body: JSON.stringify(messageData)
            }).then(() => {
                messageInput.value = ''; // Clear input
                fetchMessages(); // Fetch updated messages
            });
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Fetch messages initially
    fetchMessages();

    // Fetch messages every 3 seconds
    setInterval(fetchMessages, 3000);
});
