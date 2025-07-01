from src.project.tools.duckDBtool import profile_lookup_tool

if __name__ == "__main__":
    name_to_lookup = "Theresa Lowe"  # Replace with any valid name
    profile = profile_lookup_tool.invoke(name_to_lookup)

    print("🔎 User Profile Lookup Result:\n")
    for key, value in profile.items():
        print(f"{key}: {value}")
