# Import necessary modules
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import logging  # Import the logging module

from chat_engine import ChatEngine  # Importing the ChatEngine class

# Initialize Flask app
app = Flask(__name__)
# Initialize Bootstrap for styling
Bootstrap(app)

# Create an instance of the ChatEngine class
chat_engine = ChatEngine()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)  # Configure basic logging to a file


# Define the home route
@app.route('/')
def index():
    # Render the main chat interface
    return render_template('index.html')


# Define the route to handle user input and bot responses
@app.route('/ask', methods=['POST'])
def ask() -> object:
    try:
        # Retrieve user message from the form
        user_message: str = request.form['user_message']

        # Call the process_user_input method from the chat_engine object
        bot_response: object = chat_engine.process_user_input(user_message)

        return jsonify({'bot_response': bot_response})

    except KeyError:
        logging.error("KeyError occurred")  # Log the error
        return jsonify({'error': 'KeyError: Missing key in request'}), 400  # Return a JSON response for KeyError

    except ValueError:
        logging.error("ValueError occurred")  # Log the error
        return jsonify({'error': 'ValueError: Invalid value in request'}), 400  # Return a JSON response for ValueError

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500  # Return a JSON response for general exceptions


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
