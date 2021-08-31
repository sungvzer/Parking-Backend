from http import HTTPStatus
from flask.wrappers import Response
from flask_restful import Resource
from flask import request
from modules.parking import find_slot_containing, parking_slots, find_first_empty_slot_index
from api.auth import verify_auth
from models.auth_results import AuthResult
from api.initializer import limiter


class Home(Resource):
    """
    Home resource, accessible at the `/` endpoint via the `GET` HTTP method.

    Used to test connection
    """

    decorators = [limiter.limit("10/minute", methods=["GET"])]

    def get(self):
        return Response("Successful connection", mimetype="text/plain", status=200)

    def post(self):
        return Response("Successful connection", mimetype="text/plain", status=200)


class Park(Resource):
    """
    Parking resource, accessible at the `/park` endpoint via the `GET` HTTP method.

    Used to park a license plate.
    """

    decorators = [limiter.limit("10/minute", methods=["GET"])]

    def get(self):
        args = request.args
        license_plate = args.get('license_plate')
        auth_result = verify_auth(args)

        if auth_result != AuthResult.Success:
            if auth_result == AuthResult.NoKey:
                return {
                    'description': 'Authentication key is required to use this API'
                }, 401
            elif auth_result == AuthResult.WrongKey:
                return {
                    'description': 'Wrong authentication key'
                }, 401

        if license_plate is None:
            return {'description': 'Expected a license plate argument'}, 400

        first_empty_slot = find_first_empty_slot_index()
        if first_empty_slot == -1:
            return {'description': 'No empty slots available'}, 404

        slot_with_license_plate = find_slot_containing(license_plate)
        if slot_with_license_plate != -1:
            return {'description': f'Car with license plate {license_plate} is already parked in slot {slot_with_license_plate}'}, 403

        # By assigning a license plate, the slot is automatically considered non-empty
        parking_slots[first_empty_slot].license_plate = license_plate
        return {'license_plate': license_plate, 'slot': first_empty_slot}, 200


class Slot(Resource):
    """
    Slot resource, accessible at the `/slot` endpoint via the `GET` HTTP method.

    It is used to lookup a certain slot's information.
    """

    decorators = [limiter.limit("10/minute", methods=["GET"])]

    def get(self):
        args = request.args

        auth_result = verify_auth(args)

        if auth_result != AuthResult.Success:
            if auth_result == AuthResult.NoKey:
                return {
                    'description': 'Authentication key is required to use this API'
                }, 401
            elif auth_result == AuthResult.WrongKey:
                return {
                    'description': 'Wrong authentication key'
                }, 401

        number = args.get('number')
        if number is None:
            return {'description': 'Expected a slot number argument'}, 400

        number = int(number)
        if number < 0 or number >= len(parking_slots):
            return {'description': 'Invalid slot number'}, 400

        slot = parking_slots[number]
        return {
            'slot_number': slot.number, 'license_plate': slot.license_plate, 'is_empty': slot.is_empty()
        }, 200


class Unpark(Resource):
    """
    Unpark resource, accessible at the `/unpark` endpoint via the `GET` HTTP method.

    Removes a certain license plate from the parking.
    """

    decorators = [limiter.limit("10/minute", methods=["GET"])]

    def get(self):
        args = request.args

        auth_result = verify_auth(args)

        if auth_result != AuthResult.Success:
            if auth_result == AuthResult.NoKey:
                return {
                    'description': 'Authentication key is required to use this API'
                }, 401
            elif auth_result == AuthResult.WrongKey:
                return {
                    'description': 'Wrong authentication key'
                }, 401

        license_plate = args.get('license_plate')
        if license_plate is None:
            return {'description': 'Expected a license plate argument'}, 400

        index = find_slot_containing(license_plate)
        if index == -1:
            return {'description': 'No car with this license plate is parked here'}, 404

        slot = parking_slots[index]
        result = {'license_plate': slot.license_plate,
                  'slot_number': slot.number}

        # Free the spot
        parking_slots[index].free()
        return result, 200
