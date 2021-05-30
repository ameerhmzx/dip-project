from flask import Flask

app = Flask(__name__)
app.config.from_object('server.config')


@app.route('/')
def hello_world():
    return 'Hello, World!'
