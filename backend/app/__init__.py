from flask import Flask
from .routes import api_bp
from .models import init_db

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    init_db()
    return app