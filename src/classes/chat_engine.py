# Import the required modules and classes
import os
import sys
import json
import openai
from chat_history import ChatHistory
from user_input import UserInput
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
        self.user_input_class = UserInput()
        self.bot_response_class = BotResponse(openai.api_key)

        # Load existing conversation history using the ChatHistory class
        # The load_conversation_history method returns a list of messages
        self.conversation_history = self.chat_history.load_conversation_history()

        # Initial system message to set the context
        initial_system_message = {
            "role":
                "system",
            "content":
                "You are a customer service representative for Maker Store, specializing in CNC routing machines and CNC controllers. Your knowledge is limited to the specific "
                "products and services offered by Maker Store. Always verify your information and provide accurate details. If a question pertains to a product or service not "
                "offered by Maker Store, reply with 'I'm sorry, but I don't have information about that product. Please contact our support team for assistance.' Your tone "
                "should be friendly and informative."
        }

        # Add the initial system message to the conversation history
        self.conversation_history.append(initial_system_message)

    # Method to handle user input
    def handle_user_input(self):
        user_message = self.user_input_class.get_user_input()
        self.chat_history.check_token_limit(self.conversation_history)
        self.chat_history.add_message("user", user_message, self.conversation_history)

    # Method to generate bot response
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
            self.chat_history.log_conversation(self.conversation_history)
