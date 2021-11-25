from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from config import DATABASE_URI
from flask_migrate import Migrate
from user import user
from medicament import medicament
from purchase import purchase

app = Flask(__name__)

db = SQLAlchemy()
engine = create_engine(DATABASE_URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:root@localhost:5432/lab6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ma = Marshmallow(engine)
Session = sessionmaker(bind=engine)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
app.register_blueprint(user)
app.register_blueprint(medicament)
app.register_blueprint(purchase)
JSONIFY_PRETTYPRINT_REGULAR = False

@app.route('/')
def hello_world():
    return 'Hello World! - 15'



if __name__ == '__main__':
    app.run(debug=True)



#alembic stamp head
#alembic revision --autogenerate
#alembic upgrade head