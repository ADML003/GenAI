# Import necessary libraries for the search application
import streamlit as st  # For creating the web interface
from langchain_groq import ChatGroq  # Groq LLM for reasoning and responses
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper  # API wrappers for external services
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun  # Search tools
from langchain.agents import initialize_agent,AgentType  # Agent framework for tool coordination
from langchain.callbacks import StreamlitCallbackHandler  # Real-time display of agent thoughts
import os
from dotenv import load_dotenv  # For loading environment variables

## Creating Search Tools with API Wrappers
# ArXiv tool for research paper searches
arxiv_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)  # Limit to 1 result, 200 chars
arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)  # Create the actual search tool

# Wikipedia tool for general knowledge searches
api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)  # Limit to 1 result, 200 chars
wiki=WikipediaQueryRun(api_wrapper=api_wrapper)  # Create the Wikipedia search tool

# DuckDuckGo for general web searches
search=DuckDuckGoSearchRun(name="Search")  # General web search capability


# Streamlit UI Setup
st.title("🔎 LangChain - Chat with search")
"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""

## Sidebar for API Key Input
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Groq API Key:",type="password")  # Secure input for API key

# Initialize Chat History
# Check if messages exist in session state, if not create initial message
if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assisstant","content":"Hi,I'm a chatbot who can search the web. How can I help you?"}
    ]

# Display all previous messages in the chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

# Main Chat Interface
# When user enters a message in the chat input
if prompt:=st.chat_input(placeholder="What is machine learning?"):
    # Add user message to session state and display it
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    # Initialize the Language Model
    llm=ChatGroq(groq_api_key=api_key,model_name="llama-3.1-8b-instant",streaming=True)
    
    # Combine all available tools for the agent
    tools=[search,arxiv,wiki]  # DuckDuckGo, ArXiv, and Wikipedia

    # Create an agent that can use tools to answer questions
    search_agent=initialize_agent(
        tools,  # Available tools
        llm,    # Language model for reasoning
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Agent type that can reason and act
        handling_parsing_errors=True  # Handle any parsing errors gracefully
    )
    # ZERO_SHOT_REACT_DESCRIPTION: Agent reads tool descriptions and decides which to use

    # Generate and display the response
    with st.chat_message("assistant"):
        # StreamlitCallbackHandler shows the agent's thinking process in real-time
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        
        # Run the agent with the conversation history and callback for real-time updates
        response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        
        # Save the response to session state and display it
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)

