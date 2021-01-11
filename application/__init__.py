from flask import Flask, render_template



app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return "Hello World"
    