class ParkingSpot:
    def __init__(self, elemkey, study_area, date_time, side, unitdesc, parking_spaces, vehicle_count):
        self.key = elemkey
        self.study_area = study_area
        self.date_time = date_time
        self.extract_date_and_time()
        self.side = side
        self.unit_description = unitdesc
        self.total_spaces = int(parking_spaces)
        self.spaces_taken = int(vehicle_count)

    def extract_date_and_time(self):
        date_time = self.date_time.split()
        self.date = date_time[0]
        self.time = date_time[1]
