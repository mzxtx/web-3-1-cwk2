from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)

    # relationship
    pets = db.relationship("PetModel", backref = "user")

class ServeModel(db.Model):
    __tablename__ = "serve"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    servename = db.Column(db.String(200), nullable=False, unique=True)
    classification = db.Column(db.String(200), nullable=False, unique=False)
    obj = db.Column(db.String(200), nullable=False, unique=False)
    price = db.Column(db.Float,nullable=False,unique=False)
    introduction = db.Column(db.String(1000),nullable=True,unique=False)

class PetModel(db.Model):
    __tablename__ = "pet"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # ForeignKey
    masterid = db.Column(db.Integer, db.ForeignKey("user.id"))
    petname = db.Column(db.String(200), nullable=False, unique=False)
    species = db.Column(db.String(200), nullable=False, unique=False)
    breed = db.Column(db.String(200), nullable=False, unique=False)
    sex = db.Column(db.String(200), nullable=False, unique=False)
    birthday = db.Column(db.Date,nullable=False)

#
# class PASModel(db.Model):
#     __tablename__ = "pas"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # ForeignKey
#     petid = db.Column(db.Integer, db.ForeignKey("pet.id"))
#     serveid = db.Column(db.Integer, db.ForeignKey("serve.id"))
#     date = db.Column(db.DateTime, default=datetime.now)
#
#     # relationship
#     pet = db.relationship("PetModel", backref = "pet")
#     serve = db.relationship("ServeModel", backref="serve")

