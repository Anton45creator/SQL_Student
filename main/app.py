import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


# DATABASE = os.environ['DATABASE']
DATABASE = "postgres:123456@localhost/student"


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DATABASE}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


app = create_app()
client = app.test_client()
db = SQLAlchemy(app)
api = Api(app, prefix='/api/v1.0')
