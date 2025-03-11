from flask import Flask, request
from flask_cors import CORS
from timeit import default_timer as timer
import math

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
    return {"members": ["Sagar", "Wilson", "Eric", "Aarush"]}

# Retrieve Top 5 Links For Query Route
@app.route("/most-relevant")
def findMostRelevant():
    query = request.args.get('query')
    start = timer()
    top_5_results = retrieval.make_query(query)
    end = timer()
    total_time = end - start
    total_time = math.trunc(total_time * 1000)
    total_time = f'{total_time} ms'
    return {
        'Results': top_5_results,
        'RetrievalTime': total_time
    }



if __name__ == "__main__":
    app.run(debug=True)


