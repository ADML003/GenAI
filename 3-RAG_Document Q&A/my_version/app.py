import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
groq_api_key=os.getenv("GROQ_API_KEY")

llm=ChatGroq(groq_api_key=groq_api_key,model="Llama3-8b-8192")

prompt=ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Question:{input}

    """
    
)

st.title("RAG Document Q&A with Groq")
st.write("Upload your PDF files to the research_papers folder and ask questions!")

def create_vector_embedding():
    if "vectors" not in st.session_state:
        try:
            st.session_state.embeddings=OllamaEmbeddings(model="nomic-embed-text")
            st.session_state.loader=PyPDFDirectoryLoader("research_papers") ## Data Ingestion step
            st.session_state.docs=st.session_state.loader.load() ## Document Loading
            
            if len(st.session_state.docs) == 0:
                st.error("No PDF files found in research_papers directory!")
                return
                
            st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
            st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
            st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)
        except Exception as e:
            st.error(f"Error creating embeddings: {str(e)}")
            st.error("Make sure Ollama is running and the 'nomic-embed-text' model is available")
            st.code("Run: ollama pull nomic-embed-text")

user_prompt=st.text_input("enter your query from the research papers:")
if st.button("Document Embedding"):
    create_vector_embedding()
    st.write("Vector Database is ready")
    
import time  
if user_prompt:
    if "vectors" not in st.session_state:
        st.error("Please create vector embeddings first by clicking 'Document Embedding'")
    else:
        document_chain=create_stuff_documents_chain(llm,prompt)
        # this stuff documents chain is used to combine the documents and pass it to the llm
        # context is the key which is used to pass the documents to the llm
        retriever=st.session_state.vectors.as_retriever()
        retrieval_chain= create_retrieval_chain(retriever,document_chain)
        
        start=time.process_time()
        response=retrieval_chain.invoke({"input":user_prompt})
        print(f"Response time :{time.process_time()-start}")
        st.write(response['answer'])
    
    