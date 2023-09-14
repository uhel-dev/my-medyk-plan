document.addEventListener("DOMContentLoaded", function() {
    const slotText = document.getElementById('slotText');

    const phrases = [
        "stay healthy.",
        "save up to £782.",
        "get seen.",
        "get treated."
    ];

    slotText.innerHTML = phrases.map(text => `<div>${text}</div>`).join('');
});