#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

# Register the blueprint app_views to the Flask instance app
app.register_blueprint(app_views)


# Define a method to handle app context teardown
@app.teardown_appcontext
def teardown_appcontext(error):
    storage.close()


if __name__ == "__main__":
    import os

    # Get the host from the environment variable HBNB_API_HOST
    # or use '0.0.0.0' as default
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')

    # Get the port from the environment variable HBNB_API_PORT
    # or use 5000 as default
    port = int(os.getenv('HBNB_API_PORT', 5000))

    # Run the Flask server (app) with the specified host,
    # port, and enable threading
    app.run(host=host, port=port, threaded=True)
