// Add an event listener to handle the Enter key press
const inputElement = document.querySelector(".input input");
inputElement.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        getMessage();
    }
});

// The getMessage function to get the message from the input field and send it
function getMessage() {
    const input = document.querySelector(".input input");
    const message = input.value.trim();
    console.log(message)
    if (message !== "") {
        sendMessage("Me", message);
    }
    input.value = ""; // Clear the input field after sending the message
}

// Add an event listener to the send button to handle click
const sendButton = document.querySelector('#send');
sendButton.addEventListener('click', () => {
    getMessage();
});