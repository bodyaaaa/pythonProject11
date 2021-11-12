from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import DATABASE_URI
from models import Base,  User
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:root@localhost:5432/lab6'

@app.route('/')
def hello_world():
    return 'Hello World! - 15'

if __name__ == '__main__':
    app.run()


#alembic stamp head
#alembic revision --autogenerate
#alembic upgrade head