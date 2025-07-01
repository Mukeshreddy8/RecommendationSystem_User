import duckdb
from src.project.injection.csv_loader import load_users_data

def injection_duckdb(csv_path):
    df = load_users_data(csv_path)

    # path to your duckdb file
    db_path = "/Users/mukeshreddy/Desktop/RecommendationSytem_User/user_profiles.duckdb"
    con = duckdb.connect(database=db_path, read_only=False)
    con.register("df_view", df)
    con.execute("CREATE OR REPLACE TABLE users AS SELECT * FROM df_view")

    con.close()

if __name__ == "__main__":
    injection_duckdb("/Users/mukeshreddy/Desktop/RecommendationSytem_User/dummy_users_400_full_profile.csv")
    print("DuckDB injection completed.")



