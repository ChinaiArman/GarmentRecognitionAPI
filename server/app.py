from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def root():
    response = jsonify({'text': 'hello world'})
    return response


if __name__ == '__main__':
    app.run(debug=True, threaded=False)