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

function updateCount() {
    const count = document.querySelectorAll('.hidden-checkbox:checked').length;
    document.getElementById('count-display').innerText = `Số lượng đã chọn: ${count}`;
    const modifiContainer = document.querySelector('[name="hidden-div"]');
    modifiContainer.style.display = count > 0 ? "flex" : "none";
}
document.addEventListener("DOMContentLoaded", function () {
    updateCount();
});