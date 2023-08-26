// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Get the chat form and chat history elements
    const form = document.getElementById("chat-form");
    const chatHistory = document.getElementById("chat-history");

    // Add an event listener for form submission
    form.addEventListener("submit", function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Get the user's input from the text field
        const userInput = document.getElementById("user-input").value;

        // Create a new div element to display the user's message
        const userMessage = document.createElement("div");
        userMessage.textContent = "User: " + userInput;

        // Append the user's message to the chat history
        chatHistory.appendChild(userMessage);

        // Use the fetch API to send a POST request to the Flask app
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `user_message=${userInput}`
        })
        // Parse the JSON response from the Flask app
        .then(response => response.json())
        .then(data => {
            // Create a new div element to display the bot's message
            const botMessage = document.createElement("div");
            botMessage.textContent = "Bot: " + data.bot_response;

            // Append the bot's message to the chat history
            chatHistory.appendChild(botMessage);
        });

        // Clear the text field for the next message
        document.getElementById("user-input").value = "";
    });
});