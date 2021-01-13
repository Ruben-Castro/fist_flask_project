import os

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xabu9s\xb7(\x81Ht\xd8\x95\xd7\x1a\xf4\x1a\xcd\x10\xd0\xd7\xa7\xac\xa4ic\xf8A\x9c\x830jG\\'
    MONGODB_SETTINGS = {
        'db': 'UTA_Enrollment'
    }

#class DevConfig(BaseConfig):
