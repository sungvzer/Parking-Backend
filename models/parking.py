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
