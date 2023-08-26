# Import the OpenAI library to interact with the GPT-3 API
import openai
# Import the sys library to write to the standard output
import sys
# Import the logging library to enable logging features
import logging
# Import the time library to simulate typing delays
import time


# Define the APIHandler class
class APIHandler:

    # The __init__ method initializes the object, it's like a constructor in C#. It is called when an object of the class is created. It takes self as the first argument which
    # refers to the object itself so that we can access the object's properties and methods. You can also pass other arguments to the __init__ method, but they will be passed as
    # arguments to the object's constructor.
    def __init__(self, api_key):
        # Store the API key passed as an argument to the object
        self.api_key = api_key

        # Set the API key for the OpenAI library
        openai.api_key = self.api_key

    # Configure the logging settings
    def configure_logging(self):
        # Configure the logging settings
        logging.basicConfig(filename='chatbot.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s')

    # Method to handle special commands like "/restart" and "/exit"
    def handle_special_commands(self, command):
        # Check if the command is "/restart"
        if command == "/restart":
            return "Restarting the conversation..."
        # Check if the command is "/exit"
        elif command == "/exit":
            return "Exiting the chatbot. Goodbye!"
        else:
            # If the command is not recognized, return None
            return None

    # Method to simulate typing effect
    def simulate_typing(self, text):
        # Loop through each character in the text
        for char in text:
            # Write one character at a time to the standard output
            sys.stdout.write(char)
            # Flush the output buffer to display the character immediately
            sys.stdout.flush()
            # Introduce a short delay to simulate typing
            time.sleep(0.001)
        # Print a newline character at the end
        print()

    # Method to log the conversation history
    def log_conversation(self, conversation_history):
        # Create a log entry by joining each message in the conversation history
        log_entry = "\n".join([
            f"{message['role']}: {message['content']}"
            for message in conversation_history
        ])
        # Log the conversation using the logging library
        logging.info(f"Conversation:\n{log_entry}")
