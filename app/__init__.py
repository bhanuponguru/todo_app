from flask import Flask, render_template, request, session, redirect
from datetime import datetime
from .models import *


app=Flask(__name__)
app.secret_key="secret"
app.config['MONGODB_SETTINGS'] = {
    'db': 'event_planner',
    'host': 'localhost',
    'port': 27017
}
db.init_app(app)

@app.route("/")
def home():
    if 'user_id' in session:
        user=User.objects(id=session['user_id']).first()
        events=Event.objects(user_id=session['user_id'])
        return render_template("dashboard.html",user=user,num_events=len(events))
    return render_template("welcome.html")

@app.route("/login", methods=['get','post'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        if User.objects(email=email):
            user=User.objects(email=email).first()
            if user.password==password:
                session['user_id']=str(user.id)
                return redirect("/")
            else:
                return "Incorrect password. click <a href='/login'>here</a> to try again."
        else:
            return "User does not exist. click <a href='/register'>here</a> to register or <a href='/login'>here</a> to try again."
    return render_template("login.html")

@app.route("/logout")
def logout():
    if 'user_id' in session: session.pop('user_id')
    return redirect("/")

@app.route("/register", methods=['get','post'])
def register():
    if request.method == 'POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email=request.form['email']
        password=request.form['password']
        if User.objects(email=email):
            return "User already exists"
        else:
            user=User(first_name=first_name,last_name=last_name,email=email,password=password)
            user.save()
            return "User created successfully"
    return render_template("register.html")

@app.route("/events", methods=['get','post'])
def events():
    if 'user_id' in session:
        if request.method == 'POST':
            title=request.form['name']
            description=request.form['description']
            due_date=request.form['date']
            due_time=request.form['time']
            due=due_date+" "+due_time
            due=datetime.strptime(due,"%Y-%m-%d %H:%M")
            event=Event(title=title,description=description, due=due,user_id=session['user_id'])
            event.save()
            return "Event created successfully"
        events=Event.objects(user_id=session['user_id'])
        return render_template("events.html",events=events)
    events=Event.objects(user_id=session['user_id'])
    return render_template("events.html",events=events)


@app.route('/events/edit', methods=['post'])
def edit_event():
    if 'user_id' in session:
        event_id=request.form['event_id']
        date=request.form['date']
        time=request.form['time']
        due=datetime.strptime(date+" "+time,"%Y-%m-%d %H:%M")
        event=Event.objects(id=event_id).first()
        event.due=due
        event.save()
        return redirect("/events")
    
@app.route('/events/remove', methods=['post'])
def remove_event():
    if 'user_id' in session:
        event_id=request.form['event_id']
        event=Event.objects(id=event_id).first()
        event.delete()
        return redirect("/events")
    return redirect("/")