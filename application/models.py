import flask
from application import db


class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)


class Course(db.Document):
    courseID = db.StringField(unique=True, max_length=10)
    title = db.StringField(max_length=100)
    description = db.StringField(max_length=255)
    credits = db.IntField()
    term = db.StringField(max_length=10)


class Enrollment(db.Document):
    user_id = db.IntField()
    course_id = db.StringField(max_length=10)
