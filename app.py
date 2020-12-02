import os
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
# app.config.from_pyfile('config.py')

@app.route("/")
def hello():
    return f"{os.environ.get('TEST')"

@app.route("/<name>")
def hello_name(name):
    return f"hello {name}"

if __name__ == '__main__':
    app.run()