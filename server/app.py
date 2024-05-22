"""
Author: ``@cc-dev-65535``
Version: ``1.0.0``

Description:
This file contains the main application logic for the Garment Recognition API server.

Requirements:
This script requires the installation of the flask and flask_cors libraries.
The GarmentRecognizer class is defined in the garment_recognizer module.

Usage:
To execute this module from the root directory, run the following command:
    ``python server/app.py``
"""

from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
from garment_recognizer import GarmentRecognizer


app = Flask(__name__, template_folder="../ui/templates", static_folder="../ui/static")
CORS(app)

garment_recognizer = GarmentRecognizer()


# ERROR HANDLERS
@app.errorhandler(400)
def bad_request(
    e: Exception,
) -> tuple:
    """
    Bad request error handler.

    Args:
    -----
    e : ``Exception``
        The exception raised.
    
    Returns:
    --------
    ``tuple``
        A tuple containing the error message and error code.
    
    Notes:
    ------
    1. The function returns a tuple containing the error message and a 400 status code.
    2. The error message is extracted from the exception and converted to a string.

    Example:
    --------
    >>> e = Exception("Bad request.")
    >>> response = bad_request(e)
    >>> print(response)
    ... # {'Error': 'Bad request.'}

    Author: ``@ChinaiArman``
    """
    return {"Error": str(e)}, 400


@app.errorhandler(404)
def not_found(
    e: Exception,
) -> tuple:
    """
    Not found error handler.

    Args:
    -----
    e : ``Exception``
        The exception raised.
    
    Returns:
    --------
    ``tuple``
        A tuple containing the error message and error code.
    
    Notes:
    ------
    1. The function returns a tuple containing the error message and a 404 status code.
    2. The error message is extracted from the exception and converted to a string.

    Example:
    --------
    >>> e = Exception("Not found.")
    >>> response = not_found(e)
    >>> print(response)
    ... # {'Error': 'Not found.'}

    Author: ``@ChinaiArman``
    """
    return {"Error": str(e)}, 404


@app.errorhandler(500)
def internal_server_error(
    e: Exception,
) -> tuple:
    """
    Internal server error handler.

    Args:
    -----
    e : ``Exception``
        The exception raised.
    
    Returns:
    --------
    ``tuple``
        A tuple containing the error message and the error code.
    
    Notes:
    ------
    1. The function returns a tuple containing the error message and a 500 status code.
    2. The error message is extracted from the exception and converted to a string.

    Example:
    --------
    >>> e = Exception("Internal server error.")
    >>> response = internal_server_error(e)
    >>> print(response)
    ... # {'Error': 'Internal server error.'}

    Author: ``@ChinaiArman``
    """
    return {"Error": str(e)}, 500


@app.errorhandler(405)
def method_not_allowed(
    e: Exception,
) -> tuple:
    """
    Method not allowed error handler.

    Args:
    -----
    e : ``Exception``
        The exception raised.

    Returns:
    --------
    ``tuple``
        A tuple containing the error message.
    
    Notes:
    ------
    1. The function returns a tuple containing the error message and the error code.
    2. The error message is extracted from the exception and converted to a string.

    Example:
    --------
    >>> e = Exception("Method not allowed.")
    >>> response = method_not_allowed(e)
    >>> print(response)
    ... # {'Error': 'Method not allowed.'}

    Author: ``@ChinaiArman``
    """
    return {"Error": str(e)}, 405


# ROUTES
@app.route("/")
def root(
) -> str:
    """
    Renders the index page.

    Args:
    -----
    None.

    Returns:
    --------
    ``str``
        The index page.
    
    Notes:
    ------
    1. The function renders the index page.

    Example:
    --------
    >>> response = root()
    >>> print(response)
    ... # The index page.

    Author: ``@cc-dev-65535``
    """
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search_items(
) -> tuple:
    """
    Searches for garments by image from url.

    Args:
    -----
    None.

    Request Body:
    -------------
    url : ``str``
        The URL of the image to search for garments.
    size : ``int``
        The maximum number of items to return in the list.
    
    Returns:
    --------
    ``tuple``
        A list of matching garments in JSON format and a 200 status code.
    
    Notes:
    ------
    1. The function retrieves garments that match the provided image using the GarmentRecognizer.
    2. If the image URL is not provided, it aborts with a 400 status code and an error message.

    Example:
    --------
    >>> response = client.post("/search", json={"url": "https://url.com", "size": 5})
    >>> print(response.json)
    ... # Prints the list of matching garments in JSON format.

    Author: ``@cc-dev-65535``
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
    return jsonify(response), 200


@app.route("/items/<int:id>", methods=["GET"])
def get_item_by_id(
    id: int
) -> dict:
    """
    Retrieves a garment by its ID.

    Args:
    -----
    id : ``int``
        The ID of the garment to retrieve.

    Returns:
    --------
    ``tuple``
        The garment data in JSON format and a 200 status code.

    Notes:
    ------
    1. The function retrieves the garment with the provided ID using the GarmentRecognizer.
    2. If the garment is not found, it aborts with a 404 status code and an error message.

    Example:
    --------
    >>> response = client.get("/items/1")
    >>> print(response.json)
    ... # Prints the garment data with ID 1 in JSON format.

    Author: ``@nataliecly``
    """
    item = garment_recognizer.get_item_by_id(id)
    if item is None:
        abort(
            400,
            description="Garment not found."
        )
    return jsonify(item), 200


@app.route("/keyword_search", methods=["POST"])
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
    ``tuple``
        A list of matching garments in JSON format and a 200 status code.

    Notes:
    ------
    1. The function retrieves garments that match the provided keywords using the GarmentRecognizer.
    2. If the keywords are not provided, it aborts with a 400 status code and an error message.

    Example:
    --------
    >>> response = client.post("/items/search", json={"keywords": ["shirt", "red"]})
    >>> print(response.json)
    ... # Prints the list of matching garments in JSON format.

    Author: ``@ChinaiArman``
    """
    try:
        keywords = request.json["keywords"]
        results_size = request.json["size"]
    except KeyError:
        abort(
            400,
            description="Invalid request format. Please provide 'keywords' and 'size' in the request body.",
        )
    response = garment_recognizer.get_items_by_keywords(keywords, results_size)
    return jsonify(response), 200


@app.route("/add_item", methods=["POST"])
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
    ``tuple``
        The added garment data in JSON format and a 201 status code.

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

    Author: ``@levxxvi``
    """
    try:
        new_item = request.json
        response = garment_recognizer.insert_row(new_item)
    except KeyError:
        abort(
            400,
            description="Invalid request format. Please provide the new item details in the request body.",
        )
    return jsonify(response), 201


@app.route("/items/<int:id>", methods=["DELETE"])
def delete_item(
    id : int
) -> dict:
    """
    Deletes a garment by its ID.

    Args:
    -----
    id : ``int``
        The ID of the garment to delete.

    Returns:
    --------
    ``tuple``
        A dictionary with a success message and a 204 status code if the garment is deleted successfully.

    Notes:
    ------
    1. The function deletes the garment with the provided ID using the GarmentRecognizer.
    2. If the garment is not found, it aborts with a 404 status code and an error message.

    Example:
    --------
    >>> response = client.delete("/items/1")
    >>> print(response.json)
    ... # Prints {'message': 'Garment deleted successfully'} if the garment is deleted successfully,
    ... # 404 if not found.

    Author: ``@Ehsan138``
    """
    success = garment_recognizer.delete_row(id)
    if not success:
        abort(
            400,
            description="Garment not found."
        )
    return jsonify({'message': 'Garment deleted successfully'}), 204


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
