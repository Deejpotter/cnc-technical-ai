# chat_engine.py
# Purpose: This class handles the chat logic, including data loading and generating responses based on best practices.

# Import necessary modules
import os
import sys
import time
import openai
from chat_history import ChatHistory
from bot_response import BotResponse
from langchain.document_loaders.csv_loader import CSVLoader  # For loading CSV data
from langchain.vectorstores import FAISS  # For similarity search
from langchain.embeddings.openai import OpenAIEmbeddings  # For creating embeddings
from langchain.prompts import PromptTemplate  # For defining the prompt template
from langchain.chat_models import ChatOpenAI  # For interacting with the OpenAI API
from langchain.chains import LLMChain  # For running the logic
from dotenv import load_dotenv  # For loading environment variables


class ChatEngine:
    # Initialize the ChatEngine object
    def __init__(self):
        # Initialize the OpenAI API key
        try:
            openai.api_key = os.environ['OPENAI_API_KEY']
        except KeyError:
            sys.stderr.write("API key not found.")
            exit(1)

        # Initialize classes for user input, bot response, and chat history
        self.chat_history = ChatHistory()
        self.bot_response_class = BotResponse(openai.api_key)

        # Load existing conversation history
        self.conversation_history = self.chat_history.load_conversation_history()

        # Load environment variables
        load_dotenv()

        # Load and embed the CSV data
        loader = CSVLoader(file_path="MakerStoreTechnicalInfo.csv")
        documents = loader.load()
        embeddings = OpenAIEmbeddings()
        self.db = FAISS.from_documents(documents, embeddings)

        # Initialize the ChatOpenAI class and define the prompt template
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")
        template = """
        You Are Maker Bot.
        You are a customer service representative and sales assistant.
        You work for a company called Maker Store. Your job is to answer customer questions about the products and services offered by Maker Store.
        If someone asks if you sell a product, you should respond as if you sell all of the products that Maker Store sells. 
        I will share a customer's message with you and you will give me the best answer that I should send to this customer based on past best practices.

        You will follow all of the rules below:

        1. Response should be very similar or even identical to the past best practices in terms of length, tone of voice, logical arguments, and layout.

        2. If the best practice are irrelevant, then try to mimic the style of the best practice to customer's message

        Below is a message I received from the customer:
        {message}

        Here is a list of best practices of how we normally respond to customer in similar scenarios:
        {best_practice}

        Please write the best response that I should send to this customer:
        """

        prompt = PromptTemplate(
            input_variables=["message", "best_practice"],
            template=template
        )
        self.chain = LLMChain(llm=llm, prompt=prompt)

    # Method to capture user input from the command line
    def get_user_input(self):
        user_input = input("User: ").strip()
        if not user_input:
            print("Input cannot be empty. Please try again.")
            return self.get_user_input()
        return user_input

    # Method to handle user input and add it to the conversation history
    def handle_user_input(self):
        user_message = self.get_user_input()
        self.chat_history.check_token_limit(self.conversation_history)
        self.chat_history.add_message("user", user_message, self.conversation_history)

    # Method to generate a bot response based on best practices
    def generate_best_practice_response(self, user_message):
        similar_response = self.db.similarity_search(user_message, k=3)
        best_practice = [doc.page_content for doc in similar_response]
        bot_response = self.chain.run(message=user_message, best_practice=best_practice)
        return bot_response

    # Method to generate a bot response and add it to the conversation history
    def generate_bot_response(self):
        bot_response = self.bot_response_class.get_bot_response(self.conversation_history)
        self.chat_history.add_message("assistant", bot_response, self.conversation_history)
        print("Assistant:", bot_response)

    # This is the main method to run the chat loop
    def run_chat(self):
        while True:
            self.handle_user_input()
            self.generate_bot_response()
            self.chat_history.save_conversation_history(self.conversation_history)
