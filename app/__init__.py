from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    app.app_context().push()

    from app.users.routes import users
    from app.products.routes import products
    from app.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(main)

    return app