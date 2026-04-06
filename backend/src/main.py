import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from flask import Flask, send_from_directory
from backend.src.config.database import initialize_database
from backend.src.controllers.task_controller import task_blueprint


def create_app():
    """Factory para crear y configurar la aplicacion Flask."""
    app = Flask(__name__, static_folder='../../frontend')

    app.register_blueprint(task_blueprint, url_prefix='/api')

    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)

    initialize_database()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=5000)
