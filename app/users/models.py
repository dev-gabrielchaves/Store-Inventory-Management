from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    products = db.relationship('Product', backref='owner', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"