# Import the OpenAI library to interact with the GPT-3 API
import openai


# Define the BotResponse class
class BotResponse:

    # The __init__ method initializes the object
    def __init__(self, api_key):
        # Store the API key passed as an argument to the object
        self.api_key = api_key

    # Method to send the conversation history to the OpenAI model and get the response
    def get_bot_response(self, conversation_history: list):
        try:
            # Send the conversation history to the OpenAI model
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation_history)
            # Extract and return the bot's message content from the response
            return response['choices'][0]['message']['content']
        except Exception as e:
            # Print any exceptions that occur
            print(f"An error occurred: {e}")
            return "I'm sorry, but I'm unable to respond at the moment. Please try again later."
