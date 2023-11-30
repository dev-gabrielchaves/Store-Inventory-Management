from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This Is The Secret Key'
# Setting the URI where our database will be located
# In the case of using a sqlite database, the structure is like the following
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app) # Creating an object db, instace of the class SQLAlchemy, that will allow us to work with the database
app.app_context().push()
bcrypt = Bcrypt(app)

from app import routes # Even if it's grey, it is necessary to have this import when running the application, otherwise nothing will be shown