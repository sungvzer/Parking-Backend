from flask import Flask
from flask_restful import Resource, Api, reqparse
from models.endpoints import Park, Slot, Unpark

app = Flask(__name__)
api = Api(app)

api.add_resource(Park, '/park')

if __name__ == '__main__':
    app.run()
