from api.auth import Authenticate
from api.endpoints import Home, Park, Slot, Unpark
from api.initializer import api, app

# Endpoint setup
api.add_resource(Home, '/')
api.add_resource(Park, '/park')
api.add_resource(Unpark, '/unpark')
api.add_resource(Slot, '/slot')
api.add_resource(Authenticate, '/authenticate')

if __name__ == '__main__':
    app.run()
