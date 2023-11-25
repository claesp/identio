import os
from flask import ( Flask, render_template )

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "identio.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    from . import identifier
    from . import general
    from . import cluster
    db.init_app(app)
    app.register_blueprint(identifier.bp)
    app.register_blueprint(general.bp)
    app.register_blueprint(cluster.bp)

    return app
