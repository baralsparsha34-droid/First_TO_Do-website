from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os
from models import Costumer_Data,Flask_TO_Do,Flask_TO_Do_Completed
# import webbrowser as weber
app=Flask(__name__)
app.secret_key="DO_IT_2031"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Flask_Storage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
data_base=SQLAlchemy(app)#(db)=data_base
#Setup Login Manager
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
    return render_template("login.html")
@app.route("/",methods=["GET","POST"])
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
        return redirect("/")
    total_task=None
    return render_template("index.html",total_task=total_task)
#Route for another web.
#App route and delete function.
@app.route("/Delete/<int:sn>")
def delete(sn):
    return redirect("/")
@app.route("/Update/<int:sn>",methods=["GET","POST"])
def update(sn):
    if request.method=="POST":
        return redirect("/")
    return render_template("update.html")
@app.route("/delete_all")
def delete_all():
    with app.app_context():
        pass
    return redirect("/")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/activity")
def activity():
    return render_template("activity.html")
@app.route("/completed")
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
