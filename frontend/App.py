from flask import Flask, request, render_template
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..retrieval import query_search





def process_search(query):
    # Replace this with your actual search logic
    return [f"Result for '{query}'"]


if __name__ == '__main__':
    # app.run(debug=True)