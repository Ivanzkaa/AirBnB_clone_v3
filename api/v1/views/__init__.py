#!/usr/bin/python3
""" starting a flask web app"""


from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/apiv1')
