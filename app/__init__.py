from flask import Flask
import os
from .controllers import register_blueprints

def create_app():
    app = Flask(__name__, template_folder='views/templates')  # Specify the template folder here

    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'csv', 'ifc'}

    # Ensure the upload directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with app.app_context():
        register_blueprints(app)

    return app
