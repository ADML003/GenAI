import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
import os 

from dotenv import load_dotenv
load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]="Chatbot with Ollama"

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Kindly answer the user's questions."),
    ("user", "{question}")
])

def res(question,engine,temperature,max_tokens):
    llm=OllamaLLM(model=engine)
    output_parser=StrOutputParser()
    chain=prompt |llm|output_parser
    ans=chain.invoke({'question':question})
    return ans
 
#select the model
engine=st.sidebar.selectbox("select the model",["llama3.2:latest"])

temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7,step=0.1)
max_tokens=st.sidebar.slider("Max Tokens",min_value=100,max_value=1000, value =150)

st.write("Just ask a question to the model")

user_input=st.text_input("Your question here")
if user_input:
    res=res(user_input,engine,temperature,max_tokens)
    st.write(res)
else:
    st.write("Please enter a question")        