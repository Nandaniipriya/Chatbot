import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Q&A Chatbot with GROQ"

##Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,llm,temprature,max_tokens):
    groq_api_key = os.getenv("GROQ_API_KEY")
    llm=ChatGroq(groq_api_key=groq_api_key,model=llm)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

##Title od the app
st.title("Q&A Chatbot with GROQ")

## sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Groq API Key",type="password")

## Drop down to select various Groq models
llm=st.sidebar.selectbox("Select an Groq model",["Llama3-8b-8192","gemma2-9b-it","qwen-2.5-32b"])

## Adjust response parameter
temprature=st.sidebar.slider("Temprature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

## Main interface for user input
st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(user_input,api_key,llm,temprature,max_tokens)
    st.write(response)
    
else:
    st.write("Please provide the query")