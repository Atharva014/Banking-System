from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LoginTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_no = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    bdate = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    phoneno = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postalCode = db.Column(db.Integer, nullable=False)
    AccNo = db.Column(db.String(20), nullable=False)
    AccType = db.Column(db.String(100), nullable=False)
    AccPin = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ttype = db.Column(db.String(30), nullable=False)
    tfrom = db.Column(db.String(20), nullable=False)
    tto = db.Column(db.String(20), nullable=False)
    tamount = db.Column(db.Integer, nullable=False)
    tdatetime = db.Column(db.DateTime, nullable=False)


class BalanceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AccNo = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.String(20), nullable=False)
    AccType = db.Column(db.String(100), nullable=False)
