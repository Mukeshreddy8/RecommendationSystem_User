from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

embedder = OpenAIEmbeddings()

@tool
def recommend_similar_users(user_bio: str, skills: str, interests: str, top_k: int = 5) -> list:
    """
    Recommend similar users based on bio, skills, and interests using Qdrant vector search.
    """
    client = QdrantClient(path="qdrant_local")
    query_text = f"{user_bio}\n{skills}\n{interests}"
    query_vector = embedder.embed_query(query_text)

    results = client.search(
        collection_name="users",
        query_vector=query_vector,
        limit=top_k,
    )

    return [match.payload for match in results]



