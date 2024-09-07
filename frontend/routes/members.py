from flask import request, jsonify
from . import app
from utils.async_request import request_provider

@app.delete("/memders")
def delete_member():
    response = request_provider.delete_member_api_call()
    return jsonify({"messag":"Member deleted"}),200
