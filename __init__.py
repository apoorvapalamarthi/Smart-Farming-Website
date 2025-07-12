from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.secret_key = "454d566c45d46bc4b99b3c3c42ea38f9"

    app.register_blueprint(main)

    return app

