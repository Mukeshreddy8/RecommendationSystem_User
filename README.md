## End to End Recommendation System 

                  [👤 User (via Flask UI)]
                            │
                    (1) Enters Username
                            │
                            ▼
             ┌────────────────────────────────┐
             │      Flask Frontend Layer      │
             └──────────────┬─────────────────┘
                            │ sends input (username)
                            ▼
         ┌──────────────────────────────────────────────┐
         │             LangGraph Agentic System         │
         └─────────────────────┬────────────────────────┘
                               │
                    Input Node (Username → User Profile)
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
        ┌────────▼────────┐        ┌─────────▼─────────┐
        │  Agent 1 (Node1)│        │  Agent 2 (Node2)  │
        │ DuckDB Tool     │        │ Qdrant Tool       │
        │ "School+Company"│        │ "Vector Embedding"│
        └────────┬────────┘        └─────────┬─────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                   ┌────────────────────────┐
                   │ Agent 3 (Aggregator)   │
                   │ Merge & Summarize Data │
                   └───────────┬────────────┘
                               │
                    (3) Return Final Result
                               ▼
              ┌────────────────────────────────┐
              │   Flask UI Displays Output     │
              └────────────────────────────────┘


## Architecture Components and Descriptions

## User Input (Frontend via Flask)
Component: HTML + Flask route
Action: User enters a username in a web form and clicks “Get Recommendations”
Technology: Flask (Python), Jinja templates (HTML), possibly Bootstrap for styling
Data Flow:
username → /recommend route (Flask)
## LangGraph Agentic System (Backbone)
Technology: LangGraph + LangChain tools
Purpose: Handles logic, decision flow, and parallel execution
Entry Point: The Flask route calls a function like:
graph.invoke({"username": "u123"})
## Input Node (LangGraph)
Purpose: Receives the username → fetches user profile from DuckDB
Output: Sends full profile (name, bio, tech stack, school, company, etc.) to both agents
Role: Data preparation and input broadcasting
## Agent 1 – Node 1 (DuckDB Tool)
Technology: DuckDB SQL
Action:
Uses school + company from the user profile
Finds top 5 users with similar academic/professional background
LangChain Tool Name: profile_lookup_tool
Output: List of 5 recommended profiles (structured dictionary)
## Agent 2 – Node 2 (Qdrant Vector Search Tool)
Technology: Qdrant + OpenAI Embeddings
Action:
Uses user’s bio, skills, and interests
Converts them into embeddings
Finds semantically similar users using cosine similarity
LangChain Tool Name: recommend_similar_users
Output: Natural language explanation of user similarity (e.g., “These users share similar skills and interests in AI and backend development”)
## Agent 3 – Aggregator Node
Action:
Waits for both agent nodes to finish
Merges the two outputs (structured + text)
Optionally formats it into HTML or markdown
Technology: LangChain function or custom merging logic in Python
Output: Combined recommendation report
## Response to Frontend (Flask UI)
Action:
Aggregated output is sent back to Flask
Flask renders it into a report page (e.g., recommendations.html)
Tech: Flask templates, Jinja2