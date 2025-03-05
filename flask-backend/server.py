from flask import Flask, request
from flask_cors import CORS

import sys
import os

# Get the parent directory (cs121)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now you can import retrieval.py
import retrieval

# to run the backend server do "python3 server.py"

app = Flask(__name__)
CORS(app)

# Home Route
@app.route("/")
def home():
    return "Welcome to search engine type shi!"

# Members API Route
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

# Retrieve Top 5 Links For Query Route
@app.route("/most-relevant")
def findMostRelevant():
    query = request.args.get('query')
    top_5_results = retrieval.makeQuery(query)
    return {'Results': top_5_results}



if __name__ == "__main__":
    app.run(debug=True)


