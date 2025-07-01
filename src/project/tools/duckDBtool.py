from langchain_core.tools import tool
import duckdb

@tool
def profile_lookup_tool(user_name: str) -> dict:
    """
    🔍 Looks up a user's full profile from DuckDB by their name.
    Input: user's name (e.g., "Theresa Lowe")
    Output: dictionary of profile data, or error if not found
    """
    try:
        # Connect to the DuckDB file
        con = duckdb.connect("user_profiles.duckdb")

        # Run SQL query
        result = con.execute(f"""
            SELECT * FROM users
            WHERE name = '{user_name}'
            LIMIT 1
        """).fetchdf()

        # Close the connection
        con.close()

        # Return profile or error
        if result.empty:
            return {"error": f"No user found with name '{user_name}'"}
        return result.iloc[0].to_dict()

    except Exception as e:
        return {"error": str(e)}
