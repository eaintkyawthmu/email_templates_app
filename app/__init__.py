from flask import Flask
from config import Config
from .db import mongo_client
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Attach the MongoDB client to the app
    app.mongo = mongo_client

    # Set up logging
    if not app.debug:
        logging.basicConfig(filename='error.log', level=logging.ERROR,
                            format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                            
    # Register blueprints or routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()
