document.addEventListener('DOMContentLoaded', function() {
    const institutionTypeSelect = document.getElementById('institution_type');
    const conditionalFields = document.querySelectorAll('.conditional-field');

    institutionTypeSelect.addEventListener('change', function() {
        const selectedType = institutionTypeSelect.value;
        conditionalFields.forEach(field => {
            if (field.classList.contains(selectedType.toLowerCase())) {
                field.style.display = 'block';
            } else {
                field.style.display = 'none';
            }
        });
    });

    // Trigger change event on page load to set initial state
    institutionTypeSelect.dispatchEvent(new Event('change'));
});
