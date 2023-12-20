# CNC Technical Support Chatbot - Code Overview

## Workflow

### API Requests

- User requests are routed to appropriate functions in `routes.py`.

### Processing User Queries

- `ChatEngine` processes queries at `/ask` endpoint, using `DataManager` for vector searches.

### Generating Responses

- `ChatEngine` uses LangChain to generate a response with retrieved Q&A pairs.

### Response

- Generated response is sent back to the user.

## `app.py` - Flask Application

### App Initialization

- Import necessary modules for Flask, routing, and JSON handling.
- Import custom modules: `bp` from `routes.py`, `ChatEngine`, and `DataManager`.

### Flask App Configuration

- Configure CORS, rate limiting, and logging.
- Set up Swagger UI for API documentation.

### Blueprint Registration

- Register the `bp` blueprint from `routes.py` for routing.

### Routes

- Define routes `/`, `/spec`, and utilize `routes.py`.

### Running the App

- Start the Flask app in debug mode.

## `chat_engine.py` - Chat Engine

### Chat Initialization

- Import modules for OpenAI, LangChain, and custom classes.
- Load environment variables.

### ChatEngine Setup

- Initialize `ChatHistory` and clear conversation history.
- Create `DataManager` instance.
- Define system prompt template for OpenAI's language model.

### User Input Processing

- `process_user_input`: Process user messages and generate responses.
- `generate_best_practice`: Use `DataManager` for vector search with user's query.
- `generate_bot_response`: Generate bot response using LangChain's chain functionality.

## `data_manager.py` - Data Manager

### Data Initialization

- Connect to MongoDB and access the Q&A collection.

### CRUD Operations

- Methods for create, read, update, delete Q&A pairs in MongoDB.

### Vector Search

- `create_vector_embeddings`: Generate vector embeddings (placeholder).
- `vector_search`: Perform vector search in the database.
- `create_vector_search_index`: Create index for vector search in MongoDB.

## Key Points

- MongoDB setup with data and vector search indices is crucial.
- Implement logic for `create_vector_embeddings` in `DataManager`.
- Reliance on OpenAI's GPT model and MongoDB's Atlas Vector Search.
