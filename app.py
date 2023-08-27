# This is the main file that runs the Flask app. It starts the Flask app and defines the routes for the app.

# Import the Flask class from the flask package. Flask is a web framework for Python which is simple and lightweight.
from flask import Flask, render_template, request, jsonify
# Import the load_dotenv function from the dotenv package
from dotenv import load_dotenv
# Import the os module to access environment variables
import os
# Import the Bootstrap class from the flask_bootstrap package
from flask_bootstrap import Bootstrap
# Import the ChatHistory and BotResponse classes for handling the conversation history and bot response
from chat_history import ChatHistory
from bot_response import BotResponse

# Initialize the Flask app
app = Flask(__name__)
# Load environment variables from the .env file
load_dotenv()
# Initialize Bootstrap using the Flask app to use the Bootstrap CSS framework
Bootstrap(app)
# Load the conversation history
chat_history = ChatHistory()
# Initialize the BotResponse class, so we can access the methods of the class
bot_response_instance = BotResponse(os.getenv("OPENAI_API_KEY"))
# Load existing conversation history so the bot can continue the conversation from where it left off
conversation_history = chat_history.load_conversation_history()


# The home route. Renders the home page which contains the chatbot.
@app.route('/')
def index():
    return render_template('index.html')


# This route handles the user input to ask a question to the bot. It is called when the user clicks the "Ask" button.
@app.route('/ask', methods=['POST'])
def ask():
    # Get the user message from the request, which is entered by the user in the text input field
    user_message = request.form['user_message']

    # Add user message to conversation history, which will be used to generate the bot response
    chat_history.add_message(conversation_history, "user", user_message)

    # Update token count dynamically
    chat_history.update_token_count(conversation_history)

    # Generate bot response
    bot_response = bot_response_instance.get_bot_response(conversation_history)

    # Add bot response to conversation history
    chat_history.add_message(conversation_history, "assistant", bot_response)

    # Save updated conversation history
    chat_history.save_conversation_history(conversation_history)

    return jsonify({'bot_response': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
