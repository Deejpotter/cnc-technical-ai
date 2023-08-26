# This is the main file that runs the Flask app.
# It starts the Flask app and defines the routes for the app.

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from classes.chat_history import ChatHistory
from classes.bot_response import BotResponse
from classes.api_handler import APIHandler

# Initialize the Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Load the conversation history
chat_history = ChatHistory()

# Initialize APIHandler and BotResponse
api_handler = APIHandler(os.getenv("OPENAI_API_KEY"))
bot_response_instance = BotResponse(os.getenv("OPENAI_API_KEY"))

# Load existing conversation history
conversation_history = chat_history.load_conversation_history()


@app.route('/')
def index():
    return render_template('index.html')


# This route handles the user input to ask a question to the bot.
@app.route('/ask', methods=['POST'])
def ask():
    # Get the user message from the request, which is entered by the user in the text input field
    user_message = request.form['user_message']
    # Che
    # Add user message to conversation history, which will be used to generate the bot response
    chat_history.add_message(conversation_history, "user", user_message)

    # Call check_token_limit with the conversation history to remove old messages if the token limit is exceeded by the new message
    chat_history.check_token_limit(conversation_history)

    # Generate bot response
    bot_response = bot_response_instance.get_bot_response(conversation_history)

    # Add bot response to conversation history
    chat_history.add_message(conversation_history, "assistant", bot_response)

    # Save updated conversation history
    chat_history.save_conversation_history(conversation_history)

    return jsonify({'bot_response': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
