import openai
import os
import sys
import json
import time
import logging

try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
    sys.stderr.write()
    exit(1)

# Define the roles in the conversation
ROLES = ["system", "user", "assistant"]

# Initial system message to set the context
initial_system_message = {
    "role":
        "system",
    "content":
        "You are a customer service representative for Maker Store, specializing in CNC routing machines and CNC controllers. Your knowledge is limited to the specific products "
        "and services offered by Maker Store. Always verify your information and provide accurate details. If a question pertains to a product or service not offered by Maker "
        "Store, reply with 'I'm sorry, but I don't have information about that product. Please contact our support team for assistance.' Your tone should be friendly and "
        "informative."
}


# Function to capture user input from the command line
def get_user_input():
    # Capture user input and remove any leading/trailing whitespace
    user_input = input("User: ").strip()
    # Check if the input is empty and recursively ask for input until valid
    if not user_input:
        print("Input cannot be empty. Please try again.")
        return get_user_input()
    return user_input


# Function to add a message to the conversation history
def add_message_to_history(role, content):
    message_object = {"role": role, "content": content}
    conversation_history.append(message_object)


# File path for saving and loading conversation history
CONVERSATION_HISTORY_FILE = "conversation_history.json"


# Function to save the conversation history to a JSON file
def save_conversation_history():
    try:
        with open(CONVERSATION_HISTORY_FILE, 'w') as file:
            json.dump(conversation_history, file)
        print("Conversation history saved.")
    except Exception as e:
        print(f"An error occurred while saving the conversation history: {e}")


# Function to load the conversation history from a JSON file
def load_conversation_history():
    try:
        with open(CONVERSATION_HISTORY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("No previous conversation history found.")
        return []
    except Exception as e:
        print(f"An error occurred while loading the conversation history: {e}")
        return []


# Function to send the conversation history to the OpenAI model and get the response
def get_bot_response():
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=conversation_history)
        bot_message_content = response['choices'][0]['message']['content']
        return bot_message_content
    except Exception as e:
        print(f"An error occurred while communicating with the OpenAI model: {e}")
        return "I'm sorry, but I'm unable to respond at the moment. Please try again later."


# Function to simulate typing effect by displaying one character at a time
def simulate_typing(text):
    for char in text:
        sys.stdout.write(char)  # Write one character at a time
        sys.stdout.flush(
        )  # Flush the output buffer to display the character immediately
        time.sleep(
            0.001)  # Short delay between characters to simulate typing speed
    print()  # Print a newline character at the end


# Function to handle special commands like restart and exit
def handle_special_commands(command):
    if command == "/restart":
        print("Restarting the conversation...")
        return load_conversation_history()  # Reload the initial conversation state
    elif command == "/exit":
        print("Exiting the chatbot. Goodbye!")
        exit(0)  # Exit the program
    else:
        return None  # Return None if the command is not recognized


# Function to log conversation history
def log_conversation():
    log_entry = "\n".join([
        f"{message['role']}: {message['content']}"
        for message in conversation_history
    ])
    logging.info(f"Conversation:\n{log_entry}")


# Configure logging
logging.basicConfig(filename='chatbot.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Load existing conversation history at the start of the program
conversation_history = load_conversation_history()
# Add the initial system message to the conversation history
conversation_history.append(initial_system_message)

# Main loop to handle user input (continuing from previous code)
while True:
    user_message = get_user_input()
    add_message_to_history("user", user_message)

    # Check for special commands and handle them if detected
    special_command_result = handle_special_commands(user_message)
    if special_command_result is not None:
        conversation_history = special_command_result
        continue

    # Get the bot's response from the OpenAI model
    bot_response = get_bot_response()
    add_message_to_history("assistant", bot_response)

    # Simulate typing effect by displaying the bot's response one character at a time
    print("Assistant:")
    simulate_typing(bot_response)

    # Save and log the conversation history after each interaction
    save_conversation_history()
    log_conversation()
