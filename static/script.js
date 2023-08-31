// Define the message container element
const messageContainer = document.getElementById("message-container");

// Wait for the DOM to be fully loaded then initialize the chat application
document.addEventListener("DOMContentLoaded", function() {
    initializeChat();
});

// Initialize the chat application by adding an event listener to the form element.
function initializeChat() {
    const form = document.getElementById("chat-form");
    form.addEventListener("submit", handleFormSubmit);
}

// Handle form submission
function handleFormSubmit(event) {
    // Prevent the form from submitting
    event.preventDefault();
    // Get the user's input
    const userInput = getUserInput();
    // Display the user's message in the chat history
    displayUserMessage(userInput);
    // Clear the user input field
    clearUserInput();
    // Display a typing indicator
    displayTypingIndicator();
    // Fetch the bot's response
    fetchBotResponse(userInput);
}

// Get user input from the text field
function getUserInput() {
    return document.getElementById("user-input").value;
}

// Create a typing indicator and display it in the chat container
function displayTypingIndicator() {
    const typingIndicator = createTypingIndicator();
    messageContainer.appendChild(typingIndicator);
}

// Fetch the bot's response from the Flask app
function fetchBotResponse(userInput) {
    // Use the fetch API to post the user's message to the Flask app.
    // Pass the user's message to the fetch API as a form-encoded string.
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_message=${userInput}`
    })
    // Then, convert the response from the Flask app to JSON
    .then(response => response.json())
    // Then pass the response data to the handleBotResponse() function for further processing
    .then(data => handleBotResponse(data));
}

// Handle the bot's response
function handleBotResponse(data) {
    // Remove the typing indicator from the chat history
    removeTypingIndicator();
    // Display the bot's message in the chat history
    displayBotMessage(data.bot_response);
}

// Remove the typing indicator from the chat history
function removeTypingIndicator() {
    // Get the typing indicator element from the DOM and remove it from the message container
    const typingIndicator = document.querySelector(".typing-indicator");
    messageContainer.removeChild(typingIndicator);
}

// Display the bot's message in the chat history
function displayBotMessage(message) {
    const botMessage = createMessageElement("bot-message", "Assistant: " + message);
    messageContainer.appendChild(botMessage);
}

// Display the user's message in the chat history
function displayUserMessage(message) {
    const userMessage = createMessageElement("user-message", "You: " + message);
    messageContainer.appendChild(userMessage);
}

// Clear the user input field
function clearUserInput() {
    document.getElementById("user-input").value = "";
}

// Create a message element with a given class and text content
function createMessageElement(className, textContent) {
    const messageElement = document.createElement("div");
    messageElement.className = className;
    messageElement.textContent = textContent;
    return messageElement;
}

// Shows a typing indicator element using a div and three span elements
function createTypingIndicator() {
    // First create the div element and set the class name
    const typingIndicator = document.createElement("div");
    typingIndicator.className = "typing-indicator";
    // Then use a loop to create three span elements and append them to the div
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement("span");
        dot.className = "dot";
        typingIndicator.appendChild(dot);
    }
    return typingIndicator;
}

// Toggle the conversation list menu
function toggleMenu() {
    const menu = document.getElementById("mobile-conversation-list");
    menu.classList.toggle("show");
}

// Scroll to the bottom of the chat history
function scrollToBottom() {
  // Get the chat container element
  const chatContainer = document.getElementById("chat-container");
  // Then scroll to the bottom of the chat container.
  // Use the scrollHeight property to get the height of the entire chat container.
  chatContainer.scrollTop = chatContainer.scrollHeight;
}