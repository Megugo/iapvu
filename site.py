#!/usr/bin/env python3
from flask import Flask,request,session,render_template,redirect
import os,datetime,json,random
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "username" in session or not session['username'] in users:
            return "No username"
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.secret_key = "qwwtdstsehdfg"

users = {'admin':{'password':'123'}}
if os.path.exists("data_site.json"):
    print("loading")
    users = json.load(open("data_site.json","r")
else:
    reload()

def reload():
    print("saving json")
    json.dump(users,open("data.json","w"))

@app.route("/")
def index():
    if 'username' in session:
        return render_template("inderx_work.html",mes=session['username'],messagex=users[session["username"]]['box'],users=users)
    return render_template("index_work.html", number_of_users = len(users))

@app.route("/register")
def register():
    user = request.values['username']
    password = request.values['password']
    if username in users:
        return render_template("index_work.html", number_of_users = len(users),message="User already exists")
    else:
        users[username] = dict(password=password,box=[])
        reload()
        return render_template("index_work.html", number_of_users = len(users),message="Registered new user")

@app.route("/login",methods = ["POST"])
def login():
    user = request.values['username']
    password = request.values['password']
    if username in users:
        if user[username]['password'] == password:
            session['username'] = username
            return redirect("/")
        else:
            del session['username']
            return render_template("index_work.html", number_of_users = len(users),message="Invalid password")
    else:
        return render_template("index_work.html", number_of_users = len(users),message="No such user")
@app.route("/list")
@login_required
def listuser():
    return ",".join(users)
@app.route("/send",methods=["POST"])
@login_required
def send():
    user = request.values['username']
    message = request.values['message']
    mes = dict(frm=session['username'],message =message,date=str(datetime.datime.now()), idx=random.randint(1,6555000))
    users[username]['box'].append(mes)
    reload()
    return "Sent"
@app.route("/message/<message_idx>")
@login_required
def messages(message_idx):
    meslist = users[session['username']]['box']
    res = ""
    for mes in meslist:
        if 'idx' in mes and mes['idx'] == int(message_idx):
            return "%s) %s:%s\n" % (mes['date'],mes['frm'],mes['message'])
    return "No such message"
@app.route("logout")
def logout():
    del session['username']
    return redirect("/")
app.run(host="0.0.0.0", port=8321)

#<protocol>://<server address>:<port>/path_on_server?argument=value&arg2=val2
