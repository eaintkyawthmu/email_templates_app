from flask import Flask
from config import Config
from .db import mongo_client

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Attach the MongoDB client to the app
    app.mongo = mongo_client

    # Register blueprints or routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()
