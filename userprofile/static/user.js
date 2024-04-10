// this is for login page google aouth btn action.

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('google-oauth').addEventListener('click', function () {
        window.location.href = '/authenticate/read_email/';
    });
});



//  this is for registeration form to get the data in a list
// Adjustments for simplified registration form
document.addEventListener('DOMContentLoaded', function () {
    var formFields = document.getElementsByTagName('input');

    // Assuming the form fields are in the order of username, email, password, password confirmation,
    // and adjusting the placeholder values accordingly. Adjust the indexes if necessary.
    formFields[1].placeholder = 'Username...'; // Placeholder for username
    formFields[2].placeholder = 'Email...'; // Placeholder for email
    formFields[3].placeholder = 'Password...'; // Placeholder for password
    formFields[4].placeholder = 'Confirm Password...'; // Placeholder for password confirmation

    for (var field in formFields) {
        formFields[field].className += ' form-control'
    } // Adding Bootstrap's form-control class for styling

});
