from flask import jsonify
from api.v1.views import app_views

# Create a route '/status' on the app_views object that returns a JSON response
@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})
