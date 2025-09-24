import os
from flask import Flask
from app.routes import routes
from app.schedule import start_scheduler

app = Flask(__name__)
app.register_blueprint(routes)

start_scheduler(app)

if __name__ == "__main__":
    from waitress import serve
    port = int(os.environ.get("PORT", 3001))
    serve(app, host="0.0.0.0", port=port)
