from src.project.tools.duckDBtool import profile_lookup_tool

# Test inputs
school = "UCLA"
workplace = "Tesla"

# Invoke tool
result = profile_lookup_tool.invoke({
    "school": school,
    "workplace": workplace
})

print("🔍 Tool Output:")
print(result)

