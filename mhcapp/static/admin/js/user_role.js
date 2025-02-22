// static/admin/js/user_role.js
document.addEventListener('DOMContentLoaded', function() {
    function toggleFields() {
        var role = document.querySelector('#id_role').value;
        document.querySelectorAll('.field-age, .field-gender, .field-address, .field-speciality').forEach(function(field) {
            field.style.display = 'none';
        });
        if (role === 'patient') {
            document.querySelector('.field-age').style.display = '';
            document.querySelector('.field-gender').style.display = '';
            document.querySelector('.field-address').style.display = '';
        } else if (role === 'doctor') {
            document.querySelector('.field-speciality').style.display = '';
        }
    }
    document.querySelector('#id_role').addEventListener('change', toggleFields);
    toggleFields();
});