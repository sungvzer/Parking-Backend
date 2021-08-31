from flask import Flask
from flask_limiter.extension import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api


# App initialization
app = Flask(__name__)
limiter = Limiter(app, get_remote_address, default_limits=['2/minute'])
api = Api(app)
