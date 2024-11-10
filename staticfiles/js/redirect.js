document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        window.location.href = document.getElementById('redirect-url').getAttribute('data-url');
    }, 3000); // Redirects after 3 seconds
});
