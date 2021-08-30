from flask_restful import Resource
from flask import request
from models.parking import parking_slots


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
        if license_plate is None:
            return {'description': 'Expected a license plate argument'}, 401

        first_empty_slot = find_first_empty_slot_index()
        if first_empty_slot == -1:
            return {'description': 'No empty slots available'}, 404

        slot_with_license_plate = find_slot_containing(license_plate)
        if slot_with_license_plate != -1:
            return {'description': f'Car with license plate {license_plate} is already parked in slot {slot_with_license_plate}'}

        parking_slots[first_empty_slot].license_plate = license_plate
        return {'license_plate': license_plate, 'slot': first_empty_slot}, 200

