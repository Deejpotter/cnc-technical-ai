# Import necessary modules
from flask import Flask, jsonify, request, redirect  # Added redirect for URL redirection
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint  # Import Swagger UI blueprint
from flask_cors import CORS
from flask_limiter import Limiter
import logging
import os

# Importing the ChatEngine class for chat logic
from chat_engine import ChatEngine

# Initialize Flask app
app = Flask(__name__)
# Read allowed origins from environment variables
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '').split(',')
# Enable CORS
CORS(app, resources={r"/*": {"origins": allowed_origins}})
# Initialize Flask-Limiter to limit the number of requests that can be made to the API
limiter = Limiter(app)

# Create an instance of the ChatEngine class for chat functionalities
chat_engine = ChatEngine()

# Configure logging to log into app.log file with debug level
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Swagger UI Configuration
# URL for exposing Swagger UI (without trailing '/')
SWAGGER_URL = '/swagger'
# Our API url (can use a URL or relative path)
API_URL = '/spec'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "CNC Technical Support Chatbot API"
    }
)

# Register blueprint at URL
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Redirect root to Swagger UI
@app.route('/')
def index():
    # Redirect to Swagger UI
    return redirect('/swagger')


# Route to serve Swagger specification
@app.route("/spec")
def spec():
    # Generate Swagger spec
    swag = swagger(app)
    # API version
    swag['info']['version'] = "1.0"
    # API title
    swag['info']['title'] = "CNC Technical Support Chatbot API"
    # Return Swagger spec as JSON
    return jsonify(swag)


# Route to handle user input and bot responses
@app.route('/ask', methods=['POST'])
def ask():
    """
        This endpoint is for asking questions to the chatbot.
        ---
        parameters:
          - name: user_message
            in: formData
            type: string
            required: true
        responses:
          200:
            description: Returns the bot's response
        """
    try:
        # Retrieve user message from the form
        user_message = request.json['user_message']
        # Process user message and get bot response
        bot_response = chat_engine.process_user_input(user_message)
        # Return bot response with HTTP 200 OK
        return {'bot_response': bot_response}, 200

    except KeyError:
        # Log KeyError
        logging.error("KeyError occurred")
        # Return error with HTTP 400 Bad Request
        return {'error': 'KeyError: Missing key in request'}, 400

    except ValueError:
        # Log ValueError
        logging.error("ValueError occurred")
        # Return error with HTTP 400 Bad Request
        return {'error': 'ValueError: Invalid value in request'}, 400

    except Exception as e:
        # Log unexpected errors
        logging.error(f"An unexpected error occurred: {str(e)}")
        # Return error with HTTP 500 Internal Server Error
        return {'error': str(e)}, 500


# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
