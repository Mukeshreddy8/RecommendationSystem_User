# 📁 app.py (or src/project/ui/app.py)

# 📄 src/project/ui/app.py

from flask import Flask, render_template, request
from src.project.recommenders.State import build_graph

app = Flask(__name__)
compile_graph = build_graph()

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        user_name = request.form["user"]
        try:
            result = compile_graph.invoke({"user": user_name})
            output = result["combine_result"]
        except Exception as e:
            output = f"❌ Error: {e}"
    return render_template("index.html", output=output)



