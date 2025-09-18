import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

## Set upi the Stramlit app
st.set_page_config(page_title="Text To MAth Problem Solver And Data Serach Assistant",page_icon="🧮")
st.title("Text To Math Problem Solver Uing Google Gemma 2")

groq_api_key=st.sidebar.text_input(label="Groq API Key",type="password")


if not groq_api_key:
    st.info("Please add your Groq APPI key to continue")
    st.stop()

llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

# 🔴 WIKIPEDIA TOOL - Internet search capability for factual information
# * Purpose: Provides the agent access to world knowledge beyond its training data
# * When used: For questions requiring current facts, definitions, or encyclopedic knowledge

wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tool=Tool(
    name="wikipedia",                    # Tool identifier for the agent
    func=wikipedia_wrapper.run,          # Function to execute when tool is called  
    description="A tool for searching the Internet to find the various information on the topics mentioned"  # Agent reads this to decide when to use
)

# 🟠 MATH CALCULATOR TOOL - Handles numerical computations accurately
# * Purpose: Performs precise mathematical calculations that LLMs often get wrong
# * How it works: Converts natural language math problems into Python expressions
# * When used: For arithmetic, algebra, calculus, and any numerical computations

math_chain=LLMMathChain.from_llm(llm=llm)  # Creates a specialized math-solving chain
calculator=Tool(
    name="Calculator",
    func=math_chain.run,                   # Executes mathematical computations
    description="A tool for answering math related questions. Only input mathematical expression need to be provided."
)

# 🟤 REASONING TOOL - Logical thinking and problem breakdown
# * Purpose: Handles complex reasoning, word problems, and step-by-step explanations  
# * When used: For problems requiring logical deduction, planning, or detailed explanations
# * How it works: Uses a specialized prompt template to guide the LLM's reasoning process

prompt=""" 
you are a agent tasked for solving users mathematical question. Logically arrive at the solution and provide a detailed explanation

Question:{question}
Answer:
"""

prompt_template=PromptTemplate(
    input_variables=["question"],         # Variables that get replaced in the template
    template=prompt                       # The prompt structure with placeholders
)

chain= LLMChain(llm=llm, prompt=prompt_template)  # Combines LLM with structured prompting

reasoning_tool=Tool(
    name="reasoning tool",
    func=chain.run,                       # Executes reasoning with custom prompt
    description="A tool for answering logic-based and reasoning questions."
)

# 🟡 MULTI-AGENT SYSTEM - Agent with multiple specialized tools
# * Purpose of initialize_agent:
# ? Creates an intelligent agent that can decide which tool to use
# ? Agent reads tool descriptions and chooses the best one for each task
# ? Coordinates multiple tools (calculator, wikipedia, reasoning) automatically
# * How it works:
# ? Uses ZERO_SHOT_REACT_DESCRIPTION pattern (Reason -> Act -> Observe)
# ? Agent thinks about the problem, chooses a tool, executes it, observes result
# ? Can chain multiple tools together for complex problems

assistant_agent=initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],  # Available tools
    llm=llm,                                            # Brain of the agent
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,        # Decision-making pattern
    verbose=False,                                      # Hide internal thoughts
    handle_parsing_errors=True                          # Graceful error handling
)


# ! Important
# ? Question
# * Highlight
# TODO: Fix this bug


# 🟢 SESSION STATE MANAGEMENT - Stores chat history across Streamlit reruns
# * Why use st.session_state? 
# ? Every time user interacts with Streamlit, the entire script reruns from top to bottom
# ? Without session_state, we'd lose all previous messages on each interaction
# * How it works:
# ? session_state persists data across script reruns (like global variables)
# ? Perfect for maintaining chat conversation history
# ? Each user session gets its own session_state (isolated)

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hi, I'm a Math chatbot who can answer all your maths questions"}
    ]

# 🔵 CHAT MESSAGE DISPLAY - Shows all previous messages in chat format
# * Purpose of chat_message in Streamlit:
# ? Creates chat-like UI bubbles (user on right, assistant on left)
# ? Automatically handles message styling and positioning
# ? Makes the app look like a real chat interface (WhatsApp/ChatGPT style)

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])



# def generate_response(question):
#     res=assistant_agent.invoke({"input":question})
#     return res

# * lets start the interaction

ques=st.text_area("enter your question:","I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

if st.button("find my answer"):
    if ques:
        with st.spinner("Generating response..."):
           st.session_state.messages.append({"role":"user","content":ques})
           
           st.chat_message("user").write(ques)
           
           
           # 🟣 STREAMLIT CALLBACK HANDLER - Real-time agent thoughts display
           # * Purpose of StreamlitCallbackHandler:
           # ? Shows the agent's internal reasoning process in real-time
           # ? Displays which tool the agent chooses and why
           # ? Makes the AI's decision-making transparent to users
           # * How it works:
           # ? Captures agent's internal "thoughts" during execution
           # ? Displays them as expandable sections in Streamlit UI
           # ? expand_new_thoughts=False keeps thoughts collapsed by default
           
           st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
           res=assistant_agent.run(st.session_state.messages,callbacks=[st_cb])
           
           st.session_state.messages.append({'role':'assistant',"content":res})
           
           st.write('response:')
           st.success(res)
           
else:
    st.warning("Please enter the question")



# 🚫 Remove the old commented questions since they're now answered above
# All questions have been answered with detailed explanations in the code!


# ## Initializing the tools
# wikipedia_wrapper=WikipediaAPIWrapper()
# wikipedia_tool=Tool(
#     name="Wikipedia",
#     func=wikipedia_wrapper.run,
#     description="A tool for searching the Internet to find the vatious information on the topics mentioned"

# )

# ## Initializa the MAth tool

# math_chain=LLMMathChain.from_llm(llm=llm)
# calculator=Tool(
#     name="Calculator",
#     func=math_chain.run,
#     description="A tools for answering math related questions. Only input mathematical expression need to bed provided"
# )

# prompt="""
# Your a agent tasked for solving users mathemtical question. Logically arrive at the solution and provide a detailed explanation
# and display it point wise for the question below
# Question:{question}
# Answer:
# """

# prompt_template=PromptTemplate(
#     input_variables=["question"],
#     template=prompt
# )

# ## Combine all the tools into chain
# chain=LLMChain(llm=llm,prompt=prompt_template)

# reasoning_tool=Tool(
#     name="Reasoning tool",
#     func=chain.run,
#     description="A tool for answering logic-based and reasoning questions."
# )

# ## initialize the agents

# assistant_agent=initialize_agent(
#     tools=[wikipedia_tool,calculator,reasoning_tool],
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=False,
#     handle_parsing_errors=True
# )

# if "messages" not in st.session_state:
#     st.session_state["messages"]=[
#         {"role":"assistant","content":"Hi, I'm a MAth chatbot who can answer all your maths questions"}
#     ]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg['content'])

# ## LEts start the interaction
# question=st.text_area("Enter youe question:","I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

# if st.button("find my answer"):
#     if question:
#         with st.spinner("Generate response.."):
#             st.session_state.messages.append({"role":"user","content":question})
#             st.chat_message("user").write(question)

#             st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
#             response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb]
#                                          )
#             st.session_state.messages.append({'role':'assistant',"content":response})
#             st.write('### Response:')
#             st.success(response)

#     else:
#         st.warning("Please enter the question")









