from flask_restful import Resource
from flask import request
from models.parking import parking_slots
from auth import AuthResult, verify_auth


def find_first_empty_slot_index() -> int:
    """
    Finds the first empty parking slot

    ## Return value

        `int`:
            summary: Index of the parking slot found, `-1` if no slots are available
            example: `42`

    """
    for index in range(len(parking_slots)):
        slot = parking_slots[index]
        if slot.is_empty():
            return index
    return -1


def find_slot_containing(license_plate: str) -> int:
    """
    Find the parking slot that contains a certain license plate

    ## Attributes

        `license_plate: str`:
            summary: The license plate to be looked up
            example: `'GE219OW'`

    ## Return value

        `int`:
            summary: The parking slot number that contains the license plate, `-1` if it was not found
            example: `2`
    """

    for index in range(len(parking_slots)):
        if parking_slots[index].license_plate == license_plate:
            return index

    return -1


class Park(Resource):
    """
    Parking resource, accessible at the `/park` endpoint via the `GET` HTTP method.

    Used to park a license plate.
    """

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
