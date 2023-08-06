import os
from flask import Flask, send_file

def create_app():
    static_dir = os.environ["static_dir"]
    print(" * Static Directory: " + static_dir)
    app = Flask(__name__, static_url_path = static_dir)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        p = os.path.join(static_dir, path)
        if os.path.isdir(p) == True:
            p = os.path.join(p, "index.html")
        return send_file(p)

    return app
