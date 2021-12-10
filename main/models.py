from datetime import datetime
from main import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_birth = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    company = db.Column(db.String(20), unique=False, nullable=True)
    stocks = db.relationship('Stock', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20),unique=False, nullable=False)
    status = db.Column(db.String(5) , unique=False, nullable=False)
    amount_stoc = db.Column(db.Integer,nullable=False)
    price_stoc = db.Column(db.Integer,nullable=False)
    date_buy = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_sell = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.symbol}', '{self.amount_stoc}', '{self.price_stoc}')"

class Stockprice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol  = db.Column(db.String(20), unique=False, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    status = db.Column(db.String(10), unique=False, nullable=False)
    date_active_from = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_active_to = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price_stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Post('{self.symbol}', '{self.date_active_from}', '{self.price_stock}')"

