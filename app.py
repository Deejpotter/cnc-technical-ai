# Import necessary modules
from flask import (
    Flask,
    jsonify,
    request,
    redirect,
)  # Added redirect for URL redirection
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint  # Import Swagger UI blueprint
from flask_cors import CORS
from flask_limiter import Limiter
import logging
import os

# Importing the ChatEngine class for chat logic.
from chat_engine import ChatEngine

# Importing the QADataManager class for managing QA pairs in the database.
from data_manager import QADataManager

# Initialize Flask app
app = Flask(__name__)

# Register chat_routes blueprint to use the chat routes
from chat_routes import chat_routes
app.register_blueprint(chat_routes)

# Read allowed origins from environment variables
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "").split(",")
# Enable CORS
CORS(app, resources={r"/*": {"origins": allowed_origins}})
# Initialize Flask-Limiter to limit the number of requests that can be made to the API
limiter = Limiter(app)

# The QADataManager class is responsible for managing the QA pairs in the database.
# It should be initialized with the MongoDB URI then used by other classes to perform CRUD operations on the database.
qa_data_manager = QADataManager(os.environ["MONGO_URI"])
# Create an instance of the ChatEngine class for chat functionalities and pass the QADataManager instance to it.
chat_engine = ChatEngine(qa_data_manager)

# Configure logging to log into app.log file with debug level
logging.basicConfig(filename="app.log", level=logging.DEBUG)

# Swagger UI Configuration
# URL for exposing Swagger UI (without trailing '/')
SWAGGER_URL = "/swagger"
# Our API url (can use a URL or relative path)
API_URL = "/spec"

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        "app_name": "CNC Technical Support Chatbot API"
    },
)

# Register the blueprint with the main Flask app, making the Swagger UI available at SWAGGER_URL
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Redirect root to Swagger UI
@app.route("/")
def index():
    # Redirect to Swagger UI
    return redirect("/swagger")


# Route to serve Swagger specification
@app.route("/spec")
def spec():
    # Generate Swagger spec
    swag = swagger(app)
    # API version
    swag["info"]["version"] = "1.0"
    # API title
    swag["info"]["title"] = "CNC Technical Support Chatbot API"
    # Return Swagger spec as JSON
    return jsonify(swag)


# Route to handle user input and bot responses
@app.route("/ask", methods=["POST"])
def ask():
    """
    This endpoint is for asking questions to the chatbot.
    ---
    parameters:
      - name: user_message
        in: body
        schema:
          type: object
          required:
            - user_message
          properties:
            user_message:
              type: string
    responses:
      200:
        description: Returns the bot's response
    """
    try:
        # Retrieve user message from the form
        user_message = request.json["user_message"]
        # Process user message and get bot response
        bot_response = chat_engine.process_user_input(user_message)
        # Return bot response with HTTP 200 OK
        return {"bot_response": bot_response}, 200

    except KeyError as e:
        # Log KeyError
        logging.error(f"KeyError occurred: {str(e)}")
        # Return error with HTTP 400 Bad Request
        return {"error": "KeyError: Invalid key in request"}, 400

    except ValueError as e:
        # Log ValueError
        logging.error(f"ValueError occurred: {str(e)}")
        # Return error with HTTP 400 Bad Request
        return {"error": "ValueError: Invalid value in request"}, 400

    except Exception as e:
        # Log unexpected errors
        logging.error(f"An unexpected error occurred: {str(e)}")
        # Return error with HTTP 500 Internal Server Error
        return {"error": str(e)}, 500


# Route to add a new question-answer pair
@app.route("/add_qa", methods=["POST"])
def add_qa():
    # Extract the question and answer from the request body
    question = request.json.get("question", "")
    answer = request.json.get("answer", "")
    # Add the question-answer pair to the data manager
    qa_data_manager.add_qa_pair(question, answer)
    # Return a success status
    return jsonify({"status": "success"})

# Route to get a question-answer pair by ID
@app.route("/get_qa/<question_id>", methods=["GET"])
def get_qa(question_id):
    # Get the question-answer pair from the data manager
    qa_pair = qa_data_manager.get_qa_pair(question_id)
    # Return the question-answer pair
    return jsonify(qa_pair)

# Route to update a question-answer pair by ID
@app.route("/update_qa/<question_id>", methods=["PUT"])
def update_qa(question_id):
    # Extract the new question and answer from the request body
    new_question = request.json.get("question", "")
    new_answer = request.json.get("answer", "")
    # Update the question-answer pair in the data manager
    qa_data_manager.update_qa_pair(question_id, new_question, new_answer)
    # Return a success status
    return jsonify({"status": "success"})

# Route to delete a question-answer pair by ID
@app.route("/delete_qa/<question_id>", methods=["DELETE"])
def delete_qa(question_id):
    # Delete the question-answer pair from the data manager
    qa_data_manager.delete_qa_pair(question_id)
    # Return a success status
    return jsonify({"status": "success"})


# Run the Flask app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
