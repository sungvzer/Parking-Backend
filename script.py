from api.auth import Authenticate
from flask import Flask
from flask_restful import Api
from api.endpoints import Home, Park, Slot, Unpark

# App initialization
app = Flask(__name__)
api = Api(app)

# Endpoint setup
api.add_resource(Home, '/')
api.add_resource(Park, '/park')
api.add_resource(Unpark, '/unpark')
api.add_resource(Slot, '/slot')
api.add_resource(Authenticate, '/authenticate')

if __name__ == '__main__':
    app.run()
