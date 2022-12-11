#!/usr/bin/python3
""" starting a flask web app"""


from flask import Blueprint
from api.v1.views.states import *


app_views = Blueprint('app_views', __name__, url_prefix='/apiv1')
