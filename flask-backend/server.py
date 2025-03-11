from flask import Flask, request, jsonify
from flask_cors import CORS
from timeit import default_timer as timer
import math

import sys
import os

print("Server is up and running on port: http://localhost:8080/")


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
    return "<h1>Welcome to search engine!</h1>"

# Members API Route
@app.route("/members")
def members():
    return jsonify({
        "members": ["Sagar", "Wilson", "Eric", "Aarush"]
    })

# Retrieve Top 5 Links For Query Route
@app.route("/most-relevant")
def findMostRelevant():
    try:
        query = request.args.get('query')
        start = timer()
        top_5_results = retrieval.make_query(query)
        end = timer()
        total_time = end - start
        total_time = math.trunc(total_time * 1000)
        total_time = f'{total_time} ms'
        return jsonify({
            'Results': top_5_results,
            'RetrievalTime': total_time
        })
    except Exception as e:
        return jsonify({
            'Encountered error': str(e)
        })



if __name__ == "__main__":
    #app.run(debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)


