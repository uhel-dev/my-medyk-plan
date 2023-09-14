function togglePasswordVisibility(inputId, iconId) {
    const passwordInput = document.getElementById(inputId);
    const passwordVisibilityToggle = document.getElementById(iconId);

    // Toggle the password input type between "password" and "text"
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        // Update the icon to show the "Password hidden" state
        passwordVisibilityToggle.innerHTML = '<img src="/static/images/password-hidden.svg" alt="Password hidden" onclick="togglePasswordVisibility(\'' + inputId + '\', \'' + iconId + '\')">';
    } else {
        passwordInput.type = 'password';
        // Update the icon to show the "Password visible" state
        passwordVisibilityToggle.innerHTML = '<img src="/static/images/password-visible.svg" alt="Password visible" onclick="togglePasswordVisibility(\'' + inputId + '\', \'' + iconId + '\')">';
    }
}