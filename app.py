# Import necessary modules
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

from chat_engine import ChatEngine  # Importing the ChatEngine class

# Initialize Flask app
app = Flask(__name__)
# Initialize Bootstrap for styling
Bootstrap(app)

# Create an instance of the ChatEngine class
# This will run the __init__ method in the ChatEngine class
chat_engine = ChatEngine()


# Define the home route
@app.route('/')
def index():
    # Render the main chat interface
    return render_template('index.html')


# Define the route to handle user input and bot responses
@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Retrieve user message from the form
        user_message = request.form['user_message']

        # Call the process_user_input method from the chat_engine object
        # This method will handle the user input and generate a bot response
        bot_response = chat_engine.process_user_input(user_message)

        return jsonify({'bot_response': bot_response})

    except Exception as e:
        return jsonify({'error': str(e)})


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
