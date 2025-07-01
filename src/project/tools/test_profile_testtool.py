# src/project/tools/test_profile_testtool.py

from src.project.tools.qdrantbtool import recommend_similar_users

if __name__ == "__main__":
    input_data = {
        "user_bio": "AI researcher passionate about machine learning and education.",
        "skills": "Python, Deep Learning, NLP",
        "interests": "Education Tech, Generative AI",
        "top_k": 3
    }

    recommendations = recommend_similar_users.invoke(input_data)

    for idx, rec in enumerate(recommendations, 1):
        print(f"\n🔹 Recommendation #{idx}")
        for k, v in rec.items():
            print(f"{k}: {v}")

