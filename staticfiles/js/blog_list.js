document.addEventListener("DOMContentLoaded", () => {
    const viewMoreButtons = document.querySelectorAll('.view-more-btn');

    viewMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const expandedContent = this.previousElementSibling; // Get the expanded content div
            if (expandedContent.style.display === "none" || expandedContent.style.display === "") {
                expandedContent.style.display = "block"; // Show the full content
                this.innerHTML = "View Less <i class='fas fa-chevron-up'></i>"; // Change button text
            } else {
                expandedContent.style.display = "none"; // Hide the full content
                this.innerHTML = "View More <i class='fas fa-chevron-down'></i>"; // Change button text
            }
        });
    });
});
