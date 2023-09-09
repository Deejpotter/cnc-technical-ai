# Import necessary modules
from flask import Flask, render_template, request, jsonify
from flask_restplus import Api, Resource
import logging  # Import the logging module

from chat_engine import ChatEngine  # Importing the ChatEngine class

# Initialize Flask app
app = Flask(__name__)
api = Api(app, version='1.0', title='Chat API', description='A simple Chat API')

# Create an instance of the ChatEngine class
chat_engine = ChatEngine()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


# Define the route to handle user input and bot responses
@api.route('/ask')
class Ask(Resource):
    def post(self) -> jsonify:
        try:
            user_message = request.form['user_message']
            bot_response = chat_engine.process_user_input(user_message)
            return {'bot_response': bot_response}, 200

        except KeyError:
            logging.error("KeyError occurred")
            return {'error': 'KeyError: Missing key in request'}, 400

        except ValueError:
            logging.error("ValueError occurred")
            return {'error': 'ValueError: Invalid value in request'}, 400

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            return {'error': str(e)}, 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
