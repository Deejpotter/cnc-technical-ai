# Import the required modules and classes
import os
# Import the sys library to write to the standard output
import sys
# Import the time library to simulate typing delays
import time
# Import the OpenAI library to interact with the GPT-3 API
import openai
# Import the ChatHistory and BotResponse classes for handling the conversation history and bot response
from chat_history import ChatHistory
from bot_response import BotResponse


# Define the ChatEngine class
class ChatEngine:

    # The constructor (__init__) initializes the object when it's created
    def __init__(self):
        # Initialize the OpenAI API key
        try:
            openai.api_key = os.environ['OPENAI_API_KEY']
        except KeyError:
            sys.stderr.write("API key not found.")
            exit(1)

        # Initialize classes for user input, bot response, and chat history and store them as properties of the ChatEngine object
        # That way, we can access them from other methods in the class
        self.chat_history = ChatHistory()
        self.bot_response_class = BotResponse(openai.api_key)

        # Load existing conversation history using the ChatHistory class
        # The load_conversation_history method returns a list of messages
        self.conversation_history = self.chat_history.load_conversation_history()

        # Initial system message to set the context
        initial_system_message = {
            "role":
                "system",
            "content":
                "You are Maker Bot, a specialized customer service representative for a store called Maker Store. "
                "Your primary role is to assist customers with inquiries about CNC routing machines, CNC controllers, and other products and services exclusively offered by Maker Store. "
                "If a customer asks about a product or service, "
                "assume they are referring to Maker Store's catalog. Do not claim to lack information on a product unless it is explicitly not offered by Maker Store. "
                "Your responses should be concise, friendly, and informative. Keep your answers short and to the point, unless the customer requests more detailed "
                "information. Always prioritize accuracy and clarity in your responses."
        }

        # Add the initial system message to the conversation history
        self.conversation_history.append(initial_system_message)

    # Method to capture user input from the command line
    def get_user_input(self):
        # Capture user input and remove any leading/trailing whitespace
        user_input = input("User: ").strip()
        # Check if the input is empty and recursively ask for input until valid
        if not user_input:
            print("Input cannot be empty. Please try again.")
            return self.get_user_input()
        return user_input

    # Gets the input from the front end then checks the token limit then adds the message to the conversation history.
    def handle_user_input(self):
        user_message = self.get_user_input()
        self.chat_history.check_token_limit(self.conversation_history)
        self.chat_history.add_message("user", user_message, self.conversation_history)

    # Call the get_bot_response method of the BotResponse class to generate a response from the assistant.
    def generate_bot_response(self):
        bot_response = self.bot_response_class.get_bot_response(self.conversation_history)
        self.chat_history.add_message("assistant", bot_response, self.conversation_history)
        print("Assistant:", bot_response)

    # Method to run the chat
    def run_chat(self):
        while True:
            self.handle_user_input()
            self.generate_bot_response()
            self.chat_history.save_conversation_history(self.conversation_history)
