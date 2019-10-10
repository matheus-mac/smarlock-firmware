from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify('Hello, World!')

if __name__== "mywebserver":
    app.run(host="0.0.0.0",port=5123,debug=True)