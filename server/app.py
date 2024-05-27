"""
Author: ``@cc-dev-65535``
Version: ``1.0.0``

Description:
This module contains the main application logic for the Garment Recognition API server.
The API provides endpoints for searching garments by image and keywords, adding new garments, and editing or deleting existing garments.

Requirements:
This script requires the installation of the flask and flask_cors libraries.
This script requires the installation of the marshmallow library for data validation.
This script requires the installation of the torch library for error handling.
The GarmentRecognizer class is defined in the garment_recognizer module.

Usage:
To execute this module from the root directory, run the following command:
    ``python server/app.py``
"""

from flask import Flask, jsonify, request, abort, render_template
from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS
from garment_recognizer import GarmentRecognizer
from torch.cuda import OutOfMemoryError


app = Flask(__name__, template_folder="../ui/templates", static_folder="../ui/static")
CORS(app)

garment_recognizer = GarmentRecognizer()


# JSON VALIDATION SCHEMAS
class SemanticSearchSchema(Schema):
    url = fields.Str(required=True)
    size = fields.Int(required=True)


class KeywordSearchSchema(Schema):
    keywords = fields.List(fields.Str(), required=True)
    size = fields.Int(required=True)


class AddGarmentSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    imageUrl = fields.Str(required=True)


class EditGarmentSchema(AddGarmentSchema):
    id = fields.Str(required=True)


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
        data = SemanticSearchSchema().load(request.json)
        response = garment_recognizer.get_item_by_semantic_search(
            data["url"], data["size"]
        )
    except BadRequest:
        abort(
            400,
            description="Invalid request format. Request body is not valid JSON.",
        )
    except ValidationError:
        abort(
            400,
            description="Invalid request format. Please provide 'url' and 'size' in the request body.",
        )
    except OutOfMemoryError:
        abort(500, description="Out of memory error.")
    except Exception:
        abort(500, description="Internal server error.")
    return jsonify(response), 200


@app.route("/items/<id>", methods=["GET"])
def get_item_by_id(
    id: str
) -> tuple:
    """
    Retrieves a garment by its ID.

    Args:
    -----
    id : ``str``
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
    response = garment_recognizer.get_item_by_id(id)
    if response is None:
        abort(
            404,
            description="Garment not found."
        )
    return jsonify(response), 200


@app.route("/keyword_search", methods=["POST"])
def search_items_by_keywords(
) -> tuple:
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
    >>> response = client.post("/items/search", json={"keywords": ["shirt", "red"], "size": 5})
    >>> print(response.json)
    ... # Prints the list of matching garments in JSON format.

    Author: ``@ChinaiArman``
    """
    try:
        data = KeywordSearchSchema().load(request.json)
        response = garment_recognizer.get_items_by_keywords(
            data["keywords"], data["size"]
        )
    except BadRequest:
        abort(
            400,
            description="Invalid request format. Request body is not valid JSON.",
        )
    except ValidationError:
        abort(
            400,
            description="Invalid request format. Please provide 'keywords' and 'size' in the request body.",
        )
    except OutOfMemoryError:
        abort(500, description="Out of memory error.")
    except Exception:
        abort(500, description="Internal server error.")
    return jsonify(response), 200


@app.route("/add_item", methods=["POST"])
def add_item(
) -> tuple:
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
    ...     'name': 'new item',
    ...     'description': 'a new item',
    ...     'imageUrl': 'https://url.com',
    ... }
    >>> response = client.post("/items", json=new_item)
    >>> print(response.json)
    ... # Prints the added garment data in JSON format.

    Author: ``@levxxvi``
    """
    try:
        data = AddGarmentSchema().load(request.json)
        response = garment_recognizer.insert_row(data)
    except BadRequest:
        abort(
            400,
            description="Invalid request format. Data must contain keys: name, description, imageUrl.",
        )
    except ValidationError:
        abort(
            400,
            description="Invalid request format. Please provide the new item details in the request body.",
        )
    return jsonify(response), 201


@app.route("/items/<id>", methods=["DELETE"])
def delete_item(
    id : str
) -> tuple:
    """
    Deletes a garment by its ID.

    Args:
    -----
    id : ``str``
        The ID of the garment to delete.

    Returns:
    --------
    ``tuple``
        A tuple with a success message and a 204 status code if the garment is deleted successfully.

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
    response = garment_recognizer.delete_row(id)
    if not response:
        abort(
            400,
            description="Garment not found."
        )
    return jsonify({'message': 'Garment deleted successfully'}), 204

@app.route("/edit_item", methods=["PUT"])
def edit_item(
) -> tuple:
    """
    Edits a garment in the database.

    Args:
    -----
    None.

    Request Body:
    -------------
    item : ``dict``
        The garment data to edit.

    Returns:
    --------
    ``tuple``
        The edited garment data in JSON format and a 200 status code.

    Notes:
    ------
    1. The function edits a garment in the database using the GarmentRecognizer.
    2. If the item details are not provided, it aborts with a 400 status code and an error message.

    Example:
    --------
    >>> item = {
    ...     'id': 1,
    ...     'name': 'edited item',
    ...     'description': 'an edited item',
    ...     'imageUrl': 'https://url.com',
    ... }
    >>> response = client.put("/items", json=item)
    >>> print(response.json)
    ...

    Author: ``@levxxvi``
    """
    try:
        data = EditGarmentSchema().load(request.json)
        response = garment_recognizer.edit_row(data["id"], data)
    except BadRequest:
        abort(
            400,
            description="Invalid request format. Data must contain keys: name, description, imageUrl, id.",
        )
    except ValidationError:
        abort(
            400,
            description="Invalid request format. Please provide the item details in the request body.",
        )
    return jsonify(response), 201


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
