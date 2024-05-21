from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
from garment_recognizer import GarmentRecognizer


app = Flask(__name__, template_folder="../ui/templates", static_folder="../ui/static")
CORS(app)

garment_recognizer = GarmentRecognizer()


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.route("/")
def root():
    return render_template("index.html")


@app.post("/search")
def search_items():
    try:
        image_url = request.json["url"]
        results_size = request.json["size"]
    except KeyError:
        abort(
            400,
            description="Invalid request format. Please provide 'url' and 'size' in the request body.",
        )
    response = garment_recognizer.get_item_by_semantic_search(image_url, results_size)
    return response


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
