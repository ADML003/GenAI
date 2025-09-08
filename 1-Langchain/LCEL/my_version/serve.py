from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
from langserve import add_routes # creating APIs


groq_api=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api)

#1 prompt template

system_template="translate the text from english to {language}:"
prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system",system_template),
        ("user","{text}")
    ]
)

parser=StrOutputParser()

#. create chain
chain=prompt_template | model | parser


## app definition
app=FastAPI(title="Langchain with Groq API",version="1.0",description="A simple API server using Langchain runnable interfaces")


## adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=9999)