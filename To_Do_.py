from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os
from models import Costumer_Data,Flask_TO_Do,Flask_TO_Do_Completed,data_base
# import webbrowser as weber
app=Flask(__name__)
app.secret_key="DO_IT_2031"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Flask_Storage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
data_base.init_app(app)
#Setup Login Manager
@app.route("/sign_up",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        user_email_signup=request.form.get("user_email")
        user_name_signup=request.form.get("user_identity")
        user_password_signup=request.form.get("pass_key")
        duplicate_check=Costumer_Data.query.filter_by(email=user_email_signup).first()
        if duplicate_check:
            return redirect("/sign_up")
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
        if coustmer_login and coustmer_login.check_pass_key(user_password_login):
            session["username"]=coustmer_login.email
            session["email"]=coustmer_login.email
        return redirect("/")
    return render_template("login.html")
@app.route("/logout")
def log_out():
    session.pop("email",None)
    return redirect("/login")

@app.route("/",methods=["GET","POST"])
def dashboard():
    if session.get("username") and session.get("email"):#Acts like a security guard!
        #Creating logic to save show data in the table from html nad saving in database:
        if request.method=="POST":
            print("Posted")
            title=request.form["title"]
            about=request.form["description"]
            title = title if len(title)>0 else "None"
            about= about if len(about)>0 else "None"
            user_task=Flask_TO_Do(activity=title,description=about,user_email=session.get("email"))#type:ignore
            data_base.session.add(user_task)
            data_base.session.commit()
            return redirect("/")
        total_task=Flask_TO_Do.query.filter_by(user_email=session.get("email")).all()
        return render_template("index.html",total_task=total_task)
    return redirect("/login")
#Route for another web.
#App route and delete function.
@app.route("/Delete/<int:sn>")
def delete(sn):
    delter=Flask_TO_Do.query.filter_by(sn=sn,user_email=session.get("email")).first()
    data_base.session.delete(delter)
    data_base.session.commit()
    water_mark=Flask_TO_Do_Completed(activity=delter.activity,description=delter.description,user_email=delter.user_email)#type:ignore
    data_base.session.add(water_mark)
    data_base.session.commit()
    return redirect("/")
@app.route("/Update/<int:sn>",methods=["GET","POST"])
def update(sn):
    if request.method=="POST":
        activity=request.form.get("activity")
        about=request.form.get("description")
        updater=Flask_TO_Do.query.filter_by(sn=sn,user_email=session.get("email")).first()
        updater.activity=activity#type:ignore
        updater.description=about#type:ignore
        data_base.session.commit()
        return redirect("/")
    show_val=Flask_TO_Do.query.filter_by(sn=sn,user_email=session.get("email")).first()
    return render_template("update.html",update=show_val)
@app.route("/delete_all")
def delete_all():
    all_task=Flask_TO_Do.query.filter_by(user_email=session.get("email"))
    all_task2=Flask_TO_Do_Completed.query.filter_by(user_email=session.get("email"))
    all_task.delete()
    data_base.session.commit()
    all_task2.delete()
    data_base.session.commit()
    return redirect("/")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/activity")
def activity():
    total_task2=Flask_TO_Do.query.filter_by(user_email=session.get("email")).all()
    return render_template("activity.html",total_task2=total_task2)
@app.route("/completed")
def completed():
    total_task3=Flask_TO_Do_Completed.query.filter_by(user_email=session.get("email")).all()
    return render_template("completed.html",total_task3=total_task3)
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
