#!/usr/bin/python3
"""
Start Flask Application
"""
from api.v1.views.cities import *
from api.v1.views.states import *
from flask import Blueprint

app_views = Blueprint('app_views',  __name__, url_prefix='/api/v1')
