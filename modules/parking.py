import os
from dotenv import load_dotenv
from models.parking_slot import ParkingSlot

load_dotenv()
parking_slots_size = os.getenv("PARKING_SLOTS")

if parking_slots_size is None:
    parking_slots_size = 5
elif parking_slots_size is str:
    parking_slots_size = parking_slots_size.strip()

# Make sure it is converted into a number
parking_slots_size = int(parking_slots_size)

# Module list initialization
parking_slots = [ParkingSlot(x) for x in range(parking_slots_size)]


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


def resize_parking(size: int) -> None:
    """
    Change parking slots number.
    THIS ACTION WILL FREE ANY OCCUPIED PARKING SLOT

    ## Attributes

        `size: int`:
            summary: New parking size
            example: `2`

    """
    global parking_slots
    global parking_slots_size
    parking_slots.clear()
    parking_slots_size = size
    for x in range(size):
        parking_slots.append(ParkingSlot(x))
