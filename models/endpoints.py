from flask_restful import Resource
from flask import request
from models.parking import parking_slots
from auth import AuthResult, verify_auth


def find_first_empty_slot_index() -> int:
    for index in range(len(parking_slots)):
        slot = parking_slots[index]
        if slot.is_empty():
            return index
    return -1


def find_slot_containing(license_plate: str) -> int:
    for index in range(len(parking_slots)):
        if parking_slots[index].license_plate == license_plate:
            return index

    return -1


class Park(Resource):
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

        parking_slots[first_empty_slot].license_plate = license_plate
        return {'license_plate': license_plate, 'slot': first_empty_slot}, 200


class Slot(Resource):
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
