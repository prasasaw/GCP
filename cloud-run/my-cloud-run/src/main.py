""" hello world app"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)


def hello_there():
    return "hello there"


@app.route("/")
def hello_world():
    name = request.args.get("name", "World")
    response = jsonify({"message": f"Hello {name}!"})
    response.headers.add("Access-Control-Allow-Origin", "*") # to allow CORS
    response.headers.add("Content-Type", "application/json")
    print(response)
    return response


def start():
    print("Hellooooooo!!!")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


if __name__ == "__main__":
    start()
