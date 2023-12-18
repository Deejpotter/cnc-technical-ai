import os
import sys
import openai
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# My classes
from chat_history import ChatHistory
from qa_data_manager import QADataManager

# Load environment variables
from dotenv import load_dotenv

load_dotenv()


class ChatEngine:
    # Initialize the ChatEngine object and its properties
    def __init__(self):
        # Set the OpenAI API key
        try:
            openai.api_key = os.environ["OPENAI_API_KEY"]
        except KeyError:
            sys.stderr.write("API key not found.")
            exit(1)

        # Initialize ChatHistory
        self.chat_history = ChatHistory()

        # Clear existing conversation history and start with a clean slate
        self.chat_history.save_conversation_history([])

        # Initialize the QADataManager to manage QA pairs in the database.
        self.data_manager = QADataManager()

        # Initialize the ChatOpenAI class and define the system prompt template
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.system_template = """You Are Maker Bot. You are an assistant to the Maker Store service representative and sales staff. You work for a company called Maker Store. 
        Your job is to answer customer questions about the products and services offered by Maker Store. If someone asks if you sell a product, you should respond as if you sell all of the 
        products that Maker Store sells. If someone asks if you offer a service, you should respond as if you offer all of the services that Maker Store offers. If someone asks 
        if you can help them with a problem, you should respond as if you can help them with all of the problems that Maker Store can help with. IMPORTANT: If someone asks about 
        a product or service that Maker Store does not offer, you should respond telling them that Maker Store does not offer that product or service or cannot help them with 
        that problem. We don't want to mislead customers into thinking that Maker Store offers a product or service that it does not offer or can help them with a problem that 
        we can't help them with. If someone asks about other brands, you should tell them that we can't provide information about other brands and they should contact the 
        original manufacturer.
        
        Help answer this question:
        {message}
        
        You should stick to the best practices as closely as possible. If you can't find a best practice that matches the customer's question, you should respond
        with a response letting them know that you can't accurately answer their question.
        Here is a list of best practices of how we normally respond to customer in similar scenarios:
        {best_practice}
        
        Please format your responses using whitespace and line breaks to make it easier for the customer to read..
    
        """
        # Create a prompt template for the system prompt
        self.system_prompt = PromptTemplate(
            input_variables=["message", "best_practice"], template=self.system_template
        )
        self.chain = LLMChain(llm=llm, prompt=self.system_prompt)

    # Method to handle user input and generate bot response
    def process_user_input(self, message):
        # Add the user message to the conversation history
        self.chat_history.add_message("user", message)

        # Search for the best practices
        best_practices = self.generate_best_practice(message)
        # Generate a bot response based on best practices and user message
        bot_response = self.generate_bot_response(message, best_practices)
        return bot_response

    # Method to generate a bot response based on best practices
    def generate_best_practice(self, user_message):
        # Use DataManager instance to perform vector search
        query = {"$vectorSearch": {"query": user_message, "path": "vector"}}
        similar_responses = self.data_manager.vector_search(query).limit(3)

        best_practice = [response["answer"] for response in similar_responses]
        return best_practice

    # Method to generate a bot response based on best practices and user message
    def generate_bot_response(self, message, best_practices):
        # Run the chain to get the best practices then generate the bot response. Pass in the user message and best practices as variables in the prompt.
        bot_response = self.chain.run(message=message, best_practice=best_practices)
        # Add the bot response to the conversation history
        self.chat_history.add_message("bot", bot_response)
        return bot_response
