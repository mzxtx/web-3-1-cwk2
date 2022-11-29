from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)

class ServeModel(db.Model):
    __tablename__ = "serve"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    servename = db.Column(db.String(200), nullable=False, unique=True)
    classification = db.Column(db.String(200), nullable=False, unique=False)
    obj = db.Column(db.String(200), nullable=False, unique=False)
    price = db.Column(db.Float,nullable=False,unique=False)
    introduction = db.Column(db.String(1000),nullable=True,unique=False)