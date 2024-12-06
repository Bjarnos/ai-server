print("alive")
from flask import Flask
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://bjarnos.github.io"}})

@app.route('/')
def hello_world():
    return "hello"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
