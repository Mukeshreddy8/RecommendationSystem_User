from langchain.tools import tool
import duckdb

@tool
def profile_lookup_tool(user_name:str)->dict:
    """ 
    This tool will looks up and returns the full profile of the users from 
    """