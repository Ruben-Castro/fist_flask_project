from application import app
from flask import render_template

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template("index.html", login=False)



@app.route('/courses')
def courses():
    return "Courses Page"



@app.route('/register')
def register():
    return "Register Page"



@app.route('/login')
def login():
    return "Login Page"


