# tools/recommendation_tool.py

from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import os
from dotenv import load_dotenv

# Load environment variables (for API key)
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize embedding model and Qdrant client
embedder = OpenAIEmbeddings()
client = QdrantClient(path="qdrant_local")  # File-based Qdrant vector store


@tool
def recommend_similar_users(user_bio: str, skills: str, interests: str, top_k: int = 5) -> list:
    """
    Recommend similar users based on bio, skills, and interests using Qdrant vector search.
    Input:
        user_bio (str): Bio description of the user.
        skills (str): Skills of the user.
        interests (str): Interests of the user.
        top_k (int): Number of similar users to return.
    Output:
        List of top-k most similar user profiles (excluding the input user).
    """

    query_text = f"{user_bio} {skills} {interests}"
    query_vector = embedder.embed_query(query_text)

    # Perform semantic search
    results = client.search(
        collection_name="users",
        query_vector=query_vector,
        limit=top_k,
    )

    # Format and return results
    recommendations = []
    for match in results:
        recommendations.append(match.payload)  # `payload` contains full user profile

    return recommendations

