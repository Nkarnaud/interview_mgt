# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
# instantiate the extensions


def create_app(script_info=None):
    # App initialisation

    # instantiate the app
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    # set config
    db.init_app(app)
    migrate.init_app(app, db)
    # register endpoints
    from project.api.interviewapi import interview_blueprint
    app.register_blueprint(interview_blueprint)
    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
