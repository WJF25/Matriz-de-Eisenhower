from flask import Flask
from os import getenv
from app.configs import migration, database
from app import routes
from environs import Env

env = Env()
env.read_env()

def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JSON_SORT_KEYS"] = False

    database.init_app(app)
    migration.init_app(app)
    routes.init_app(app)

    return app
