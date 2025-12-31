from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os
# import webbrowser as weber
app=Flask(__name__)
app.secret_key="DO_IT_2031"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Flask_Storage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
data_base=SQLAlchemy(app)#(db)=data_base
class Flask_TO_Do_Completed(data_base.Model):
    sn=data_base.Column(data_base.Integer,primary_key=True)
    activity=data_base.Column(data_base.String(125),nullable=False)
    description=data_base.Column(data_base.String(250),nullable=False)
    created_time=data_base.Column(data_base.Date,default=date.today)
    def __repr__(self) -> str:
        return  "{0}-{1}-{2}".format(self.sn,self.activity,self.created_time)
class Flask_TO_Do(data_base.Model):
    sn=data_base.Column(data_base.Integer,primary_key=True)
    activity=data_base.Column(data_base.String(125),nullable=False)
    description=data_base.Column(data_base.String(250),nullable=False)
    created_time=data_base.Column(data_base.Date,default=date.today)
    def __repr__(self) -> str:
        return  "{0}-{1}-{2}".format(self.sn,self.activity,self.created_time)
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
        task=Flask_TO_Do(activity=title,description=about) # type: ignore
        data_base.session.add(task)
        data_base.session.commit()
        return redirect("/")
    total_task=Flask_TO_Do.query.all()
    return render_template("index.html",total_task=total_task)
#Route for another web.
@app.route("/services")
def services():
    return"It's a place to provide you services"
#App route and delete function.
@app.route("/Delete/<int:sn>")
def delete(sn):
    deleter=data_base.session.get(Flask_TO_Do,sn)
    data_base.session.delete(deleter)
    task3=Flask_TO_Do_Completed(activity=deleter.activity,description=deleter.description) # type: ignore
    data_base.session.add(task3)
    data_base.session.commit()
    data_base.session.commit()
    return redirect("/")
@app.route("/Update/<int:sn>",methods=["GET","POST"])
def update(sn):
    if request.method=="POST":
        title=request.form["title"]
        about=request.form["description"]
        update=Flask_TO_Do.query.filter_by(sn=sn).first()
        update.activity=title #type: ignore
        update.description=about  #type: ignore
        data_base.session.commit()
        return redirect("/")
    show_val=Flask_TO_Do.query.filter_by(sn=sn).first()
    return render_template("update.html",update=show_val)
@app.route("/delete_all")
def delete_all():
    with app.app_context():
        data_base.drop_all()
        data_base.create_all()
    return redirect("/")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/activity")
def activity():
    total_task2=Flask_TO_Do.query.all()
    return render_template("activity.html",total_task2=total_task2)
@app.route("/completed")
def completed():
    total_task3=Flask_TO_Do_Completed.query.all()
    return render_template("completed.html",total_task3=total_task3)
# @app.route("/search",methods=["GET","POST"])
# def web_source():
#     if request.method=="POST":
#         web=request.form.get("link")
#         weber.open(web) #type: ignore
#     return redirect("/")
#App route and sort function
#Executing in only this file
if __name__=="__main__":
    with app.app_context():
        data_base.create_all()
    ported=int(os.environ.get("PORT",2031))
    app.run(debug=False,host='0.0.0.0',port=ported,)

