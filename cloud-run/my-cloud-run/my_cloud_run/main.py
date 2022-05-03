import os

from flask import Flask, request

app = Flask(__name__)

def hello_there():
    return "hello there"

@app.route('/')
def hello_world():
    name = request.args.get('name', 'World')
    return f'Hello {name}!'

def start():
    print("Hellooooooo!!!")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    start()
