from flask import Flask
from config import BaseConfig
from flask_mongoengine import MongoEngine
from flask_restplus import Api


api = Api()
app = Flask(__name__)
app.config.from_object(BaseConfig)

db = MongoEngine()
db.init_app(app)
api.init_app(app)


from application import routes
