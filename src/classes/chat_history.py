# Import the JSON library to handle JSON files
import json


# Define the ChatHistory class
class ChatHistory:

    # The __init__ method initializes the object, it's like a constructor in C#. It is called when an object of the class is created. It takes self as the first argument which
    # refers to the object itself so that we can access the object's properties and methods. You can also pass other arguments to the __init__ method, but they will be passed as
    # arguments to the object's constructor.
    def __init__(self, history_file="conversation_history.json"):
        self.history_file = history_file
        self.token_count = 0  # Initialize token count

    # Method to roughly estimate the token count for a message
    def estimate_tokens(self, message):
        # Roughly estimate the token count for a message
        return len(message.split()) + len(message)

    # Check if the token count is over the limit including the new message
    def check_token_limit(self, conversation_history):
        while self.token_count > 4096:  # GPT-3.5-turbo's maximum token limit
            removed_message = conversation_history.pop(0)
            removed_tokens = self.estimate_tokens(removed_message['content'])
            self.token_count -= removed_tokens

    # Method to load the conversation history from a JSON file
    def load_conversation_history(self):
        try:
            # Open the JSON file in read mode
            with open(self.history_file, 'r') as file:
                # Load and return the conversation history
                return json.load(file)
        except FileNotFoundError:
            # Return an empty list if the file is not found
            return []
        except Exception as e:
            # Print any other exceptions that occur
            print(f"An error occurred: {e}")
            return []

    # Method to save the conversation history to a JSON file
    def save_conversation_history(self, conversation_history):
        try:
            # Open the JSON file in write mode
            with open(self.history_file, 'w') as file:
                # Save the conversation history to the file
                json.dump(conversation_history, file)
        except Exception as e:
            # Print any exceptions that occur
            print(f"An error occurred: {e}")

    # Method to add a message to the conversation history
    def add_message(self, conversation_history, role, content):
        message = {"role": role, "content": content}
        message_tokens = self.estimate_tokens(content)
        self.token_count += message_tokens  # Update the running token count
        self.check_token_limit(conversation_history)  # Check if we're over the limit
        conversation_history.append(message)
