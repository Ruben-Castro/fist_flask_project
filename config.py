import os

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    MONGODB_SETTINGS = {
        'db': 'UTA_Enrollment'
    }

#class DevConfig(BaseConfig):
