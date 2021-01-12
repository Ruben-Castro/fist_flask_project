import os

class BaseConfig(object):
    SECRET_KY = os.environ.get('SECRET_KEY') or "secret_string"
    MONGODB_SETTINGS = {
        'db': 'UTA_Enrollment'
    }

#class DevConfig(BaseConfig):
