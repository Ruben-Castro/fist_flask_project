import os

class BaseConfig(object):
    SECRET_KY = os.environ.get('SECRET_KEY') or "secret_string"
    

#class DevConfig(BaseConfig):
