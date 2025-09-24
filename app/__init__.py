from flask import Flask
from app.routes import routes
from app.schedule import start_scheduler

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)
    start_scheduler(app)
    return app
