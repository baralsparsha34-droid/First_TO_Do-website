from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt as bt
from datetime import date
import os
# import webbrowser as weber
app=Flask(__name__)
app.secret_key="DO_IT_2031"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Flask_Storage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
data_base=SQLAlchemy()#(db)=data_base
data_base_url = os.environ.get('DATABASE_URL', 'sqlite:///Flask_Storage.db')
if data_base_url.startswith("postgres://"):
    database_url = data_base_url.replace("postgres://", "postgresql://", 1)
class Costumer_Data(data_base.Model):
    sn=data_base.Column(data_base.Integer,primary_key=True)
    email = data_base.Column(data_base.String(150), unique=True, nullable=False)
    username = data_base.Column(data_base.String(150), unique=True, nullable=False)
    password = data_base.Column(data_base.String(150), unique=True, nullable=False)
    def __init__(self,email,username,password) -> None:
        self.email=email
        self.username=username
        raw_password=password.encode('utf-8')
        self.password=bt.hashpw(raw_password,bt.gensalt())
    def check_pass_key(self,pass_key:str)->bool:#Password are saved in hashed form  not in the exact words we type for security of user.
        return bt.checkpw(pass_key.encode('utf-8'),self.password)
class Flask_TO_Do_Completed(data_base.Model):
    sn=data_base.Column(data_base.Integer,primary_key=True)
    activity=data_base.Column(data_base.String(125),nullable=False)
    description=data_base.Column(data_base.String(250),nullable=False)
    created_time=data_base.Column(data_base.Date,default=date.today)
    user_email = data_base.Column(data_base.String(100), nullable=False)
    def __repr__(self) -> str:
        return  "{0}-{1}-{2}".format(self.sn,self.activity,self.created_time)
class Flask_TO_Do(data_base.Model):
    sn=data_base.Column(data_base.Integer,primary_key=True)
    activity=data_base.Column(data_base.String(125),nullable=False)
    description=data_base.Column(data_base.String(250),nullable=False)
    created_time=data_base.Column(data_base.Date,default=date.today)
    user_email = data_base.Column(data_base.String(100), nullable=False)
    def __repr__(self) -> str:
        return  "{0}-{1}-{2}".format(self.sn,self.activity,self.created_time)