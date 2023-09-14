// Function to validate the password
function validatePassword() {
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;

    const registerBtn = document.getElementById('register-btn');

    const atLeast10Characters = document.getElementById("at-least-10-characters-validation-rule")
    const includeANumber = document.getElementById("include-a-number-validation-rule")
    const includeAnUppercase = document.getElementById("include-an-uppercase-validation-rule")
    const includeALowercase = document.getElementById("include-a-lowercase-validation-rule")
    const bothPasswordsMatch = document.getElementById("both-passwords-matching-validation-rule")

    const isAtLeast10Chars = password.length >= 10;
    const hasANumber = /\d/.test(password);
    const hasAnUppercase = /[A-Z]/.test(password);
    const hasALowercase = /[a-z]/.test(password);
    const hasBothPasswordMatch = confirm_password.length >= 10 && password === confirm_password

    atLeast10Characters.src = password.length === 0 ? "/static/images/grey-info.svg" : (isAtLeast10Chars ? "/static/images/tick.svg" : "/static/images/error.svg");
    includeANumber.src = password.length === 0 ? "/static/images/grey-info.svg" : (hasANumber ? "/static/images/tick.svg" : "/static/images/error.svg");
    includeAnUppercase.src = password.length === 0 ? "/static/images/grey-info.svg" : (hasAnUppercase ? "/static/images/tick.svg" : "/static/images/error.svg");
    includeALowercase.src = password.length === 0 ? "/static/images/grey-info.svg" : (hasALowercase ? "/static/images/tick.svg" : "/static/images/error.svg");
    bothPasswordsMatch.src = password.length === 0 ? "/static/images/grey-info.svg" : (hasBothPasswordMatch ? "/static/images/tick.svg" : "/static/images/error.svg");

    registerBtn.disabled = !isAtLeast10Chars || !hasANumber || !hasAnUppercase || !hasALowercase || !hasBothPasswordMatch;
}


function init() {
    document.getElementById('password').addEventListener('input', validatePassword);
    document.getElementById('confirm_password').addEventListener('input', validatePassword);
}

document.addEventListener('DOMContentLoaded', init);

