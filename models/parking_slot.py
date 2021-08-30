class ParkingSlot:
    def __init__(self, number):
        self.license_plate = ""
        self.number = number

    def is_empty(self):
        if self.license_plate is None or self.license_plate == "":
            return True
        else:
            return False

    def free(self):
        self.license_plate = ""

    def __str__(self) -> str:
        if self.is_empty():
            return f"ParkingSlot[{self.number} - EMPTY]"
        return f"ParkingSlot[{self.number} - {self.license_plate}]"
