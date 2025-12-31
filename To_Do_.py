from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt as bt
from datetime import date
import os
# import webbrowser as weber
app=Flask(__name__)
app.secret_key="DO_IT_2031"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Flask_Storage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
data_base=SQLAlchemy(app)#(db)=data_base
#Setup Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"#type:ignore
@login_manager.user_loader
def load_user(user_id):
    return Costumer_Data.query.get(int(user_id))
class Costumer_Data(data_base.Model,UserMixin):
    sn=data_base.Column(data_base.Integer,primary_key=True)
    email = data_base.Column(data_base.String(150), unique=True, nullable=False)
    username = data_base.Column(data_base.String(150), unique=True, nullable=False)
    password = data_base.Column(data_base.String(150), unique=True, nullable=False)
    tasks = data_base.relationship('Flask_TO_Do', backref='owner', lazy=True)
    def __init__(self,email,username,password):
        self.password=generate_password_hash(password)
        self.username=username
        self.email=email
    def check_passkey(self,password)->bool :
        return check_password_hash(self.password,password)
    def get_id(self):
        return str(self.sn)

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
@app.route("/sign_up",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        user_email_signup=request.form.get("user_email")
        user_name_signup=request.form.get("user_identity")
        user_password_signup=request.form.get("pass_key")
        coustmer_signup=Costumer_Data(email=user_email_signup,username=user_name_signup,password=user_password_signup)#type:ignore
        data_base.session.add(coustmer_signup)
        data_base.session.commit()
        return redirect("/login")
    return render_template("sing_up.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        user_email_login=request.form.get("user_email")
        user_password_login=request.form.get("pass_key")
        coustmer_login=Costumer_Data.query.filter_by(email=user_email_login).first()
        if coustmer_login and coustmer_login.check_passkey(user_password_login):
            login_user(coustmer_login)
            return redirect("/")
        else:
            return render_template("login.html",error="Incorrect Password or Username")
    return render_template("login.html")
@app.route("/",methods=["GET","POST"])
@login_required
def welcome():
    #Creating logic to save show data in the table from html nad saving in database:
    if request.method=="POST":
        print("Posted")
        title=request.form["title"]
        about=request.form["description"]
        if len(title)>0:
            title=title
        else:
            title="None"
        if len(about)>0:
            about=about
        else:
            about="None"
        current_task=Flask_TO_Do(activity=title,description=about,user_id=current_user.sn)#type:ignore
        data_base.session.add(current_task)
        data_base.session.commit()
        return redirect("/")
    total_task=Flask_TO_Do.query.filter_by(user_id=current_user.sn).all()
    return render_template("index.html",total_task=total_task)
#Route for another web.
#App route and delete function.
@app.route("/Delete/<int:sn>")
@login_required
def delete(sn):
    deleter=data_base.session.get(Flask_TO_Do,sn)
    data_base.session.delete(deleter)
    return redirect("/")
@app.route("/Update/<int:sn>",methods=["GET","POST"])
@login_required
def update(sn):
    if request.method=="POST":
        title=request.form["title"]
        about=request.form["description"]
        return redirect("/")
    return render_template("update.html")
@app.route("/delete_all")
@login_required
def delete_all():
    with app.app_context():
        data_base.drop_all()
        data_base.create_all()
    return redirect("/")
@app.route("/about")
@login_required
def about():
    return render_template("about.html")
@app.route("/activity")
@login_required
def activity():
    return render_template("activity.html")
@app.route("/completed")
@login_required
def completed():
    return render_template("completed.html")
# @app.route("/search",methods=["GET","POST"])
# def web_source():
#     if request.method=="POST":
#         web=request.form.get("link")
#         weber.open(web) #type: ignore
#     return redirect("/")
#App route and sort function
#Executing in only this file
with app.app_context():
        data_base.create_all()
if __name__=="__main__":
    ported=int(os.environ.get("PORT",2031))
    app.run(debug=False,host='0.0.0.0',port=ported,)
