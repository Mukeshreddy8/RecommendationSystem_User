from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from src.project.tools.qdrantbtool import recommend_similar_users
from src.project.tools.duckDBtool import profile_lookup_tool

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

## binding tools
llm=ChatOpenAI(model="gpt-4o")
tools=[recommend_similar_users,profile_lookup_tool]
bind_tools=llm.bind_tools(tools)

## creating nodes
def node1(input:str):
    
