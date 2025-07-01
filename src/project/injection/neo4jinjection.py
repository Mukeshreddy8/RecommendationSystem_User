from neo4j import GraphDatabase
from src.project.injection.csv_loader import load_users_data

def injection_neo4j(csv_path):
    df = load_users_data(csv_path)
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "your-password"))

    def add_user(tx, user_id, name, school, company):
        tx.run(
            "MERGE (u:User {user_id: $user_id}) "
            "SET u.name = $name, u.school = $school, u.company = $company",
            user_id=user_id, name=name, school=school, company=company
        )

    def add_connection(tx, uid1, uid2):
        tx.run(
            "MATCH (a:User {user_id: $uid1}), (b:User {user_id: $uid2}) "
            "MERGE (a)-[:CONNECTED_TO]->(b)",
            uid1=uid1, uid2=uid2
        )

    with driver.session() as session:
        for _, row in df.iterrows():
            session.write_transaction(add_user, row["user_id"], row["name"], row["school"], row["company"])
            for conn in str(row["connections"]).split(","):
                session.write_transaction(add_connection, row["user_id"], conn.strip())

