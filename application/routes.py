from application import app, db
from flask import render_template, request, Response, json, redirect, flash, url_for
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term="Spring 2021"):
    courseData = Course.objects.order_by("courseID")
    return render_template(
        "courses.html", courseData=courseData, courses=True, term=term
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(
            user_id=user_id, email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.save()
        flash("you are successfully registered.", "success")

        return redirect(url_for("login"))
    else:
        flash("Sorry, your registration failed. Please try again.", "danger")

    return render_template("register.html", title="Register", register=True, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            return redirect(url_for("index"))
        else:
            flash("Sorry, Something whent wrong", "danger")

    return render_template("login.html", title="Login", login=True, form=form)


@app.route("/enrollement", methods=["GET", "POST"])
def enrollment():
    courseID = request.form.get("courseId")
    courseTitle = request.form.get("title")

    user_id = 1

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(
                f"Oops! You are already registered in this course{courseTitle}!",
                "danger",
            )
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success")
            

    classes = list(
        User.objects.aggregate(
            *[
                {
                    "$lookup": {
                        "from": "enrollment",
                        "localField": "user_id",
                        "foreignField": "user_id",
                        "as": "r1",
                    }
                },
                {
                    "$unwind": {
                        "path": "$r1",
                        "includeArrayIndex": "r1_id",
                        "preserveNullAndEmptyArrays": False,
                    }
                },
                {
                    "$lookup": {
                        "from": "course",
                        "localField": "r1.courseID",
                        "foreignField": "courseID",
                        "as": "r2",
                    }
                },
                {"$unwind": {"path": "$r2", "preserveNullAndEmptyArrays": False}},
                {"$match": {"user_id": user_id}},
                {"$sort": {"courseID": 1}},
            ]
        )
    )

    
    return render_template(
        "enrollment.html", enrollment=True, title="Enrollment", classes=classes
    )


@app.route("/api/")
@app.route("/api/<int:idx>")
def api(idx=None):
    if idx == None:
        jdata = courseData
    else:
        jdata = courseData[idx]

    return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
    users = User.objects.all()
    return render_template("user.html", users=users)