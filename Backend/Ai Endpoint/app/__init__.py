from flask import Flask
from config import Config
from .databaseWatcher import start_watcher

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    with app.app_context():
        start_watcher(app)

    @app.route('/')
    def index():
        return {"message": "Flask IoT Backend is running", "watcher": "active"}, 200

    return app