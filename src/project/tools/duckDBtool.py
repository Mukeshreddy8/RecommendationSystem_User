from langchain_core.tools import tool
import duckdb

@tool
def profile_lookup_tool(school: str, workplace: str) -> list:
    """
    🔍 Fetches users from DuckDB with matching school or company.
    """
    try:
        con = duckdb.connect("user_profiles.duckdb")
        result = con.execute(f"""
            SELECT name, school, company FROM users
            WHERE school = '{school}' OR company = '{workplace}'
            LIMIT 5
        """).fetchdf()
        con.close()
        return result.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

