from application import app, db, api
from flask import render_template, request, Response, json, redirect, flash, url_for, session, jsonify
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from flask_restplus import Resource
from application.queries import user_classes_query








#########################################################################

@api.route('/api', '/api/')
class GetAndPost(Resource):
    
    def get(self):
        return jsonify(User.objects.all())
    
    def post(self):
        data = api.payload
        user = User(user_id=data['user_id'], email= data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()

        return jsonify(User.objects(user_id = data['user_id']))


@api.route('/api/<int:idx>')
class GetUpdateDelete(Resource):
    
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))
    
    def put(self, idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        user = User.objects(user_id=idx)
    
        return jsonify(user)


    def delete(self, idx):
        User.objects(user_id=idx).delete()

        return jsonify("user is deleted!")





#########################################################################

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
    if session.get('username'):
        return redirect(url_for('index'))

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

        #check if the user is now in the database 
        new_user = User.objects(user_id = user_id).first()

        if new_user:
            flash("you are successfully registered.", "success")
            return redirect(url_for("login"))
        
        flash("Sorry, your registration failed. Please try again.", "danger")

       
       
    

    return render_template("register.html", title="Register", register=True, form=form)



@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            return redirect(url_for("index"))
        else:
            flash("Sorry, Something whent wrong", "danger")

    return render_template("login.html", title="Login", login=True, form=form)


@app.route("/enrollement", methods=["GET", "POST"])
def enrollment():
    # if the user is not logged in then they cant access enrollment information 
    if  not session.get('username'):
        return redirect(url_for('login'))

    courseID = request.form.get("courseId")
    courseTitle = request.form.get("title")

    user_id = session.get('user_id')

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
            

    classes = user_classes_query(user_id)
    return render_template(
        "enrollment.html", enrollment=True, title="Enrollment", classes=classes
    )




@app.route("/user")
def user():
    users = User.objects.all()
    return render_template("user.html", users=users)