from flask import Blueprint, request

chat_routes = Blueprint('chat_routes', __name__)

@chat_routes.route("/ask", methods=["POST"])
def ask():
    # Your existing /ask route code goes here

