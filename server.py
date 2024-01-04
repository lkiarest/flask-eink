from flask import Flask, send_file

from utils.utils import draw

app = Flask(__name__)

@app.route("/")
def hello_world():
    result = draw()
    return send_file(result, mimetype='image/jpeg')
