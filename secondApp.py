import streamlit as st
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

# Vectorise the sales response csv data
# First, get the data from the csv file
loader = CSVLoader(file_path="MakerStoreTechnicalInfo.csv")
# Then, load the data into the documents object
documents = loader.load()
# The OpenAIEmbeddings class is used to create embeddings for the documents by vectorising the tokens
embeddings = OpenAIEmbeddings()
# FAISS is a vector store that allows us to perform similarity search
db = FAISS.from_documents(documents, embeddings)


# Perform a similarity search on the database to retrieve the best practices
def retrieve_info(query):
    # First, get the top 3 most similar documents
    similar_response = db.similarity_search(query, k=3)
    # Then, get the page content from the documents so we don't get the metadata.
    # Loop through the documents and append the page content to an array.
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array


# The ChatOpenAI class is used as a wrapper for the OpenAI API
# Set the temperature to 0 so the model will stick to what it has learned from the training data.
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

# Define the prompt template with the input variables that will be passed into the prompt
template = """
You are a customer service representative and sales assistant.
You work for a company called Maker Store. Your job is to answer customer questions about the products and services offered by Maker Store. 
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

chain = LLMChain(llm=llm, prompt=prompt)


# Generate a response based on the best practices that were retrieved from the similarity search
def generate_response(message):
    best_practice = retrieve_info(message)
    response = chain.run(message=message, best_practice=best_practice)
    return response


# 5. Build an app with streamlit
def main():
    st.set_page_config(
        page_title="Customer response generator", page_icon=":bird:")

    st.header("Customer response generator :bird:")
    message = st.text_area("customer message")

    if message:
        st.write("Generating best practice message...")

        result = generate_response(message)

        st.info(result)


if __name__ == '__main__':
    main()
