from application import app
from flask import Flask

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return "Hello World"