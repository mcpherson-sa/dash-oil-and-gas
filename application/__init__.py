import os
import sys
import logging

from flask import Flask
import flask_appbuilder
from flask_appbuilder import AppBuilder, SQLA
from flask_assets import Environment

"""
 Logging configuration
"""
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

# application = Flask(__name__)
# application.config.from_object("config")
db = SQLA()
app_builder = AppBuilder()


def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        from .assets import compile_static_assets

        db.init_app(app)

        app_builder.init_app(app, db.session)
        from . import views  # noqa
        app_builder.post_init()

        from .dash.dashboard import init_dashboard
        app = init_dashboard(app)

        compile_static_assets(assets)

    return app


