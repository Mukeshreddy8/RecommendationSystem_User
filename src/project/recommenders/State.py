## 📁 File: src/project/langgraph_core/graph.py
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
import duckdb
import json

from src.project.tools.duckDBtool import profile_lookup_tool
from src.project.tools.qdrantbtool import recommend_similar_users

llm = ChatOpenAI(model="gpt-4o")
bind_tool = llm.bind_tools([profile_lookup_tool, recommend_similar_users])

class State(TypedDict):
    user: str
    school: str
    workplace: str
    bio: str
    skills: str
    interests: str
    duckdb_result: list
    qdrant_result: str
    combine_result: str

def profile_loader_node(state: State):
    user = state["user"]
    con = duckdb.connect("user_profiles.duckdb")
    result = con.execute(f"""
        SELECT * FROM users
        WHERE name = '{user}'
        LIMIT 1
    """).fetchdf()
    con.close()

    if result.empty:
        return {"error": f"No user found: {user}"}

    row = result.iloc[0]
    return {
        "user": user,
        "school": row["school"],
        "workplace": row["company"],
        "bio": row["bio"],
        "skills": row["skills"],
        "interests": row["interests"]
    }

def duckdb_node(state: State):
    results = profile_lookup_tool.invoke({
        "school": state["school"],
        "workplace": state["workplace"]
    })

    if isinstance(results, dict) and "error" in results:
        return {"duckdb_result": []}

    return {"duckdb_result": results}

def qdrant_node(state: State):
    results = recommend_similar_users.invoke({
        "user_bio": state["bio"],
        "skills": state["skills"],
        "interests": state["interests"]
    })

    if isinstance(results, dict) and "error" in results:
        return {"qdrant_result": "No semantic recommendations found."}

    # 📏 Let the LLM explain each match based on state + results
    explanation_prompt = f"""
    You are an intelligent recommendation assistant.

    The user has the following profile:
    - Bio: {state['bio']}
    - Skills: {state['skills']}
    - Interests: {state['interests']}

    Based on semantic similarity, the following users were retrieved:
    {json.dumps(results, indent=2)}

    For each user, explain **why** they were recommended — based on shared skills, experience, or interests.
    Use 1-2 sentences per user and keep it natural and concise.
    """

    msg = bind_tool.invoke(explanation_prompt)
    return {"qdrant_result": msg.content}

def aggregator_node(state: State):
    duckdb_matches = state.get("duckdb_result", [])
    qdrant_text = state.get("qdrant_result", "No semantic recommendations found.")

    # 🟡 DuckDB Explanation
    if duckdb_matches:
        duckdb_text = "These users share your school or workplace:\n"
        for match in duckdb_matches:
            reasons = []
            if match.get("school") == state["school"]:
                reasons.append(f"both studied at {state['school']}")
            if match.get("company") == state["workplace"]:
                reasons.append(f"both worked at {state['workplace']}")
            duckdb_text += f"- {match['name']}: You {', and '.join(reasons)}.\n"
    else:
        duckdb_text = "No relevant school/workplace matches found."

    return {
        "combine_result": (
            f"\U0001f50d Report for `{state['user']}`\n\n"
            f"\U0001f7e1 DuckDB Insights:\n{duckdb_text}\n\n"
            f"\U0001f535 Qdrant Insights:\n{qdrant_text}"
        )
    }

def build_graph():
    builder = StateGraph(State)
    builder.add_node("load_profile", profile_loader_node)
    builder.add_node("duckdb", duckdb_node)
    builder.add_node("qdrant", qdrant_node)
    builder.add_node("combine", aggregator_node)

    builder.add_edge(START, "load_profile")
    builder.add_edge("load_profile", "duckdb")
    builder.add_edge("load_profile", "qdrant")
    builder.add_edge("duckdb", "combine")
    builder.add_edge("qdrant", "combine")
    builder.add_edge("combine", END)

    return builder.compile()
