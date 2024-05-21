"""
"""

from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
from garment_recognizer import GarmentRecognizer


app = Flask(__name__, template_folder="../ui/templates", static_folder="../ui/static")
CORS(app)

garment_recognizer = GarmentRecognizer()


@app.errorhandler(400)
def bad_request(e):
    """
    """
    return jsonify(error=str(e)), 400


@app.route("/")
def root():
    """
    """
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search_items():
    """
    """
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


@app.route("/items/<int:id>", methods=["GET"])
def get_item_by_id(id):
    """
    Retrieves a garment by its ID.

    Args:
    -----
    id : ``int``
        The ID of the garment to retrieve.

    Returns:
    --------
    ``json``
        The garment data in JSON format.

    Notes:
    ------
    1. The function retrieves the garment with the provided ID using the GarmentRecognizer.
    2. If the garment is not found, it aborts with a 404 status code and an error message.

    Example:
    --------
    >>> response = client.get("/items/1")
    >>> print(response.json)
    ... # Prints the garment data with ID 1 in JSON format.

    Author: ``@Ehsan138``
    """
    item = garment_recognizer.get_item_by_id(id)
    if item is None:
        abort(404, description="Garment not found.")
    return jsonify(item)


@app.route("/items/search", methods=["POST"])
def search_items_by_keywords():
    """
    Searches for garments by keywords.

    Args:
    -----
    None.

    Request Body:
    -------------
    keywords : ``list``
        A list of keywords to search for garments.

    Returns:
    --------
    ``json``
        A list of matching garments in JSON format.

    Notes:
    ------
    1. The function retrieves garments that match the provided keywords using the GarmentRecognizer.
    2. If the keywords are not provided, it aborts with a 400 status code and an error message.

    Example:
    --------
    >>> response = client.post("/items/search", json={"keywords": ["shirt", "red"]})
    >>> print(response.json)
    ... # Prints the list of matching garments in JSON format.

    Author: ``@Ehsan138``
    """
    try:
        keywords = request.json["keywords"]
    except KeyError:
        abort(400, description="Invalid request format. Please provide 'keywords' in the request body.")
    response = garment_recognizer.get_items_by_keywords(keywords)
    return jsonify(response)


@app.route("/items", methods=["POST"])
def add_item():
    """
    Adds a new garment to the database.

    Args:
    -----
    None.

    Request Body:
    -------------
    new_item : ``dict``
        The new garment data.

    Returns:
    --------
    ``json``
        The added garment data in JSON format.

    Notes:
    ------
    1. The function adds a new garment to the database using the GarmentRecognizer.
    2. If the item details are not provided, it aborts with a 400 status code and an error message.

    Example:
    --------
    >>> new_item = {
    ...     'id': 3,
    ...     'name': 'new item',
    ...     'description': 'a new item',
    ...     'imageUrl': 'https://url.com',
    ...     'keywordDescriptions': 'new, item'
    ... }
    >>> response = client.post("/items", json=new_item)
    >>> print(response.json)
    ... # Prints the added garment data in JSON format.

    Author: ``@Ehsan138``
    """
    try:
        new_item = request.json
    except KeyError:
        abort(400, description="Invalid request format. Please provide the item details in the request body.")
    response = garment_recognizer.add_item(new_item)
    return jsonify(response), 201


@app.route("/items/<int:id>", methods=["DELETE"])
def delete_item(id):
    """
    """
    success = garment_recognizer.delete_item(id)
    if not success:
        abort(404, description="Garment not found.")
    return '', 204


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
