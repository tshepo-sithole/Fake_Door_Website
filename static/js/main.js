const sliderBar = document.getElementById('sliderBar');
const sliderBadge = document.getElementById('sliderBadge');
const container = document.getElementById('compSlider');

let currentMode = "BEFORE";

function syncLabel() {
    const barRect = sliderBar.getBoundingClientRect();
    const containerRect = container.getBoundingClientRect();

    const barPositionX = barRect.left - containerRect.left;
    const percentage = (barPositionX / containerRect.width) * 100;

    if (percentage < 14) {
        if (currentMode !== "BEFORE") {
            currentMode = "BEFORE";
            sliderBadge.textContent = "BEFORE";
            sliderBadge.classList.remove('after-mode');
        }
    } else {
        if (currentMode !== "AFTER") {
            currentMode = "AFTER";
            sliderBadge.textContent = "AFTER";
            sliderBadge.classList.add('after-mode');
        }
    }
    requestAnimationFrame(syncLabel);
}

if (sliderBar && sliderBadge && container) {
    requestAnimationFrame(syncLabel);
}
// contact form
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const messageInput = document.getElementById('message');
const submitButton = document.getElementById('submitButton');

if (nameInput && emailInput && messageInput && submitButton) {
    function checkInputs() {
        if (nameInput.value.trim() !== '' && emailInput.value.trim() !== '' && messageInput.value.trim() !== '') {
            submitButton.removeAttribute('disabled');
            submitButton.style.opacity = '1';
            submitButton.style.cursor = 'pointer';
        } else {
            submitButton.setAttribute('disabled', 'true');
            submitButton.style.opacity = '0.65';
            submitButton.style.cursor = 'not-allowed';
        }
    }

    checkInputs();

    nameInput.addEventListener('input', checkInputs);
    emailInput.addEventListener('input', checkInputs);
    messageInput.addEventListener('input', checkInputs);
}

// download form
// Wrap each page's logic independently
document.addEventListener("DOMContentLoaded", function() {
    const nameInput = document.getElementById('download_name');
    const emailInput = document.getElementById('download_email');
    const submitButton = document.getElementById('download_submitButton');

    if (nameInput && emailInput && submitButton) {
        function checkInputs() {
            const isValid = nameInput.value.trim() !== '' && emailInput.value.trim() !== '';
            submitButton.disabled = !isValid;
            submitButton.style.opacity = isValid ? '1' : '0.65';
            submitButton.style.cursor = isValid ? 'pointer' : 'not-allowed';
        }

        checkInputs();
        nameInput.addEventListener('input', checkInputs);
        emailInput.addEventListener('input', checkInputs);
    }
});
