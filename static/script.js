// Get the message container element
const messageContainer = document.getElementById("message-container");

// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    initializeChat();
});

// Initialize the chat application
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
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_message=${userInput}`
    })
    .then(response => response.json())
    .then(data => handleBotResponse(data));
}

// Handle the bot's response
function handleBotResponse(data) {
    removeTypingIndicator();
    displayBotMessage(data.bot_response);
}

// Remove the typing indicator from the chat history
function removeTypingIndicator() {
    const typingIndicator = document.querySelector(".typing-indicator");
    messageContainer.removeChild(typingIndicator);
}

// Display the bot's message in the chat history
function displayBotMessage(message) {
    const botMessage = createMessageElement("bot-message", "Assistant: " + message);
    messageContainer.appendChild(botMessage);
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

// Create a typing indicator element
function createTypingIndicator() {
    const typingIndicator = document.createElement("div");
    typingIndicator.className = "typing-indicator";
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement("span");
        dot.className = "dot";
        typingIndicator.appendChild(dot);
    }
    return typingIndicator;
}

// Function to toggle the sliding menu
function toggleMenu() {
    const menu = document.getElementById("mobile-conversation-list");
    menu.classList.toggle("show");
}

// Display the user's message in the chat history
function displayUserMessage(userInput) {
  const userMessage = document.createElement("div");
  userMessage.className = "user-message";
  userMessage.textContent = "You: " + userInput;
  messageContainer.appendChild(userMessage);
  scrollToBottom();
}

// Display the bot's message in the chat history
function displayBotMessage(botResponse) {
  const botMessage = document.createElement("div");
  botMessage.className = "bot-message";
  botMessage.textContent = "Assistant: " + botResponse;
  messageContainer.appendChild(botMessage);
  scrollToBottom();
}

// Scroll to the bottom of the chat history
function scrollToBottom() {
  const chatContainer = document.getElementById("chat-container");
  chatContainer.scrollTop = chatContainer.scrollHeight;
}