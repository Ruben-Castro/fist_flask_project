from application import app, db
from flask import render_template, request, Response, json

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term="Spring 2021"):
    return render_template(
        "courses.html", courseData=courseData, courses=True, term=term
    )


@app.route("/register")
def register():
    return render_template("register.html", register=True)


@app.route("/login")
def login():
    return render_template("login.html", login=True)


@app.route("/enrollement", methods=["GET", "POST"])
def enrollment():
    id = request.form.get("courseId")
    title = request.form.get("title")
    term = request.form.get("term")

    return render_template(
        "enrollment.html",
        enrollment=True,
        data={"id": id, "title": title, "term": term},
    )


@app.route("/api/")
@app.route("/api/<int:idx>")
def api(idx=None):
    if idx == None:
        jdata = courseData
    else:
        jdata = courseData[idx]

    return Response(json.dumps(jdata), mimetype="application/json")


class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)

@app.route('/user')
def user():
    users = User.objects.all()
    return render_template("user.html", users=users)