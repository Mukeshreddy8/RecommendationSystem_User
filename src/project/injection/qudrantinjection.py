from dotenv import load_dotenv
load_dotenv()

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from langchain_openai import OpenAIEmbeddings
from src.project.injection.csv_loader import load_users_data

def injection_qdrant(csv_path):
    df = load_users_data(csv_path)

    embedder = OpenAIEmbeddings()
    client = QdrantClient(path="qdrant_local")

    if client.collection_exists("users"):
        client.delete_collection("users")

    client.create_collection(
        collection_name="users",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )

    for idx, row in df.iterrows():
        text = f"{row['bio']} {row['skills']} {row['interests']}"
        vector = embedder.embed_query(text)
        payload = row.to_dict()
        client.upsert(
            collection_name="users",
            points=[PointStruct(id=idx, vector=vector, payload=payload)]
        )

    print("✅ Qdrant injection complete.")

if __name__ == "__main__":
    injection_qdrant("/Users/mukeshreddy/Desktop/RecommendationSytem_User/dummy_users_400_full_profile.csv")



