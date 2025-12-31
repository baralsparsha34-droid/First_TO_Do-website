from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt as bt
from datetime import date
# import webbrowser as weber
app=Flask(__name__)
app.secret_key="DO_IT_2031"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Flask_Storage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
data_base=SQLAlchemy(app)#(db)=data_base
class Costumer_Data(data_base.Model):
    sn=data_base.Column(data_base.Integer,primary_key=True)
    email = data_base.Column(data_base.String(150), unique=True, nullable=False)
    username = data_base.Column(data_base.String(150), unique=True, nullable=False)
    password = data_base.Column(data_base.String(150), unique=True, nullable=False)
    def __init__(self,email,username,password) -> None:
        self.email=email
        self.username=username
        self.password=bt.hashpw(password.encode("utf-8"),bt.gensalt())
    def pass_key(self,pass_key)->bool:#Password are saved in hashed form  not in the exact words we type for security of user.
        return bt.checkpw(pass_key,self.password)
class Flask_TO_Do_Completed(data_base.Model):
    sn=data_base.Column(data_base.Integer,primary_key=True)
    activity=data_base.Column(data_base.String(125),nullable=False)
    description=data_base.Column(data_base.String(250),nullable=False)
    created_time=data_base.Column(data_base.Date,default=date.today)
    user_id = data_base.Column(data_base.Integer, data_base.ForeignKey('costumer__data.sn'), nullable=False)
    def __repr__(self) -> str:
        return  "{0}-{1}-{2}".format(self.sn,self.activity,self.created_time)
class Flask_TO_Do(data_base.Model):
    sn=data_base.Column(data_base.Integer,primary_key=True)
    activity=data_base.Column(data_base.String(125),nullable=False)
    description=data_base.Column(data_base.String(250),nullable=False)
    created_time=data_base.Column(data_base.Date,default=date.today)
    user_id = data_base.Column(data_base.Integer, data_base.ForeignKey('costumer__data.sn'), nullable=False)
    def __repr__(self) -> str:
        return  "{0}-{1}-{2}".format(self.sn,self.activity,self.created_time)