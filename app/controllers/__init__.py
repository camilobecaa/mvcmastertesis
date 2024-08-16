from flask import Blueprint

main = Blueprint('main', __name__)

from .main_controller import *

def register_blueprints(app):
    app.register_blueprint(main)
