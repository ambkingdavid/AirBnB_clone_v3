#!/usr/bin/python3
from flask import Blueprint
# Wildcard import of everything in the package api.v1.views.index
from api.v1.views.index import *


# Create a variable app_views which is an instance of
# Blueprint with a url prefix of '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
