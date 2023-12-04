from Include import *
from client_SMTP import *
from client_POP3 import *
from test_client import *

class Singleton(type):
    _instances = {}

    def __init__(cls, name, bases, methods):
        cls._instance = None
        super().__init__(name, bases, methods)

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class User(metaclass=Singleton):
    def __init__(self, SMTPclient: Client_SMTP, POP3client: Client_POP3):
        self.SMTPclient = SMTPclient
        self.POP3client = POP3client

    def reset(self, SMTPclient: Client_SMTP, POP3client: Client_POP3):
        self.SMTPclient = SMTPclient
        self.POP3client = POP3client
