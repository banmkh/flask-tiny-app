document.addEventListener("DOMContentLoaded", function() {
    let flashMessages = document.querySelectorAll(".flash-message");
    if (flashMessages.length > 0) {
        flashMessages.forEach((msg, index) => {
            if (index !== flashMessages.length - 1) {
                msg.style.display = "none";
            }
        });
        let lastMessage = flashMessages[flashMessages.length - 1];
        setTimeout(() => {
            lastMessage.style.opacity = "0";
            setTimeout(() => { lastMessage.remove(); }, 500);
        }, 3000);
    }
});
