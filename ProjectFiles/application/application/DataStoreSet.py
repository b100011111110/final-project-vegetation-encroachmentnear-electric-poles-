import csv
import math

class UniqueIDGenerator:
    def __init__(self):
        self.counter = 0

    def generate_id(self):
        self.counter += 1
        return self.counter

class DataStore:
    def __init__(self):
        self.data = {}
        self.id_generator = UniqueIDGenerator()

    def add_value(self, place, top_left, bottom_right, point_a, point_b):
        unique_id = self.id_generator.generate_id()
        self.data[unique_id] = {
            "place": place,
            "top_left": top_left,
            "bottom_right": bottom_right,
            "point_a": point_a,
            "point_b": point_b
        }
        return unique_id

    def sort_data(self):
        sorted_data = sorted(self.data.values(), key=lambda x: (x["place"], x["point_a"], x["point_b"]))
        return sorted_data

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        # Calculate the great-circle distance between two points on the Earth's surface
        R = 6371  # Radius of the Earth in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def get_nearest_line_segment_id(self, place, target_point):
        min_distance = float('inf')
        nearest_segment_id = None

        for unique_id, entry in self.data.items():
            if entry["place"] == place:
                # Calculate distance between target point and line segment AB
                distance = self.distance_to_line_segment(entry["point_a"], entry["point_b"], target_point)
                if distance < min_distance:
                    min_distance = distance
                    nearest_segment_id = unique_id
        return nearest_segment_id, min_distance * 1000  # Convert distance from kilometers to meters

    def distance_to_line_segment(self, point_a, point_b, target_point):
        # Calculate distance between a point and a line segment
        lat1, lon1 = point_a
        lat2, lon2 = point_b
        lat3, lon3 = target_point

        d_lat_ab = lat2 - lat1
        d_lon_ab = lon2 - lon1
        d_lat_ac = lat3 - lat1
        d_lon_ac = lon3 - lon1
        d_lat_bc = lat3 - lat2
        d_lon_bc = lon3 - lon2

        dot_ab_ac = d_lat_ab * d_lat_ac + d_lon_ab * d_lon_ac
        dot_ba_bc = -d_lat_ab * d_lat_bc - d_lon_ab * d_lon_bc

        if dot_ab_ac <= 0:
            return self.haversine_distance(lat1, lon1, lat3, lon3)
        elif dot_ba_bc <= 0:
            return self.haversine_distance(lat2, lon2, lat3, lon3)
        else:
            distance = abs(d_lat_ab * d_lon_ac - d_lon_ab * d_lat_ac) / math.sqrt(d_lat_ab ** 2 + d_lon_ab ** 2)
            return distance

    def get_value(self, unique_id):
        return self.data.get(unique_id, None)

    def export_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Place", "Top Left", "Bottom Right", "Point A", "Point B"])
            for unique_id, entry in self.data.items():
                writer.writerow([unique_id, entry["place"], entry["top_left"], entry["bottom_right"], entry["point_a"], entry["point_b"]])

    def convertStrToTuple(self,str):
        str = str.lstrip('(')
        str = str.rstrip(')')
        str = str.split(',')
        return float(str[0]),float(str[1])
        
    def import_from_csv(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                place = row["Place"]
                top_left = row["Top Left"]
                bottom_right = row["Bottom Right"]
                point_a = row["Point A"]
                point_b = row["Point B"]
                self.add_value(place, top_left, bottom_right, point_a, point_b)
        for i in self.data:
            self.data[i]["top_left"] = self.convertStrToTuple(self.data[i]["top_left"])
            self.data[i]["bottom_right"] = self.convertStrToTuple(self.data[i]["bottom_right"])
            self.data[i]["point_a"] = self.convertStrToTuple(self.data[i]["point_a"])
            self.data[i]["point_b"] = self.convertStrToTuple(self.data[i]["point_b"])
# Example usage:

# if __name__ == "__main__":
#     store = DataStore()
#     store.add_value("Nitte", (13.1836393, 74.9377762), (13.1823240, 74.9391743), (13.1834781,74.9382653), (13.1824829,74.9382841))
#     store.add_value("Nitte", (13.1804760, 74.9322961), (13.1792047, 74.9327511), (13.1801400, 74.9328341), (13.1792047, 74.9327511))
#     store.add_value("Nitte", (13.1762453, 74.9301518), (13.1759166, 74.9309925), (13.1760525, 74.9302892), (13.1762360, 74.9308400))

#     place = input("Enter the place: ")
#     latitude = float(input("Enter the latitude of the target point: "))
#     longitude = float(input("Enter the longitude of the target point: "))
#     target_point = (latitude, longitude)

#     nearest_segment_id, min_distance = store.get_nearest_line_segment_id(place, target_point)
#     if nearest_segment_id:
#         print("Nearest line segment ID found:", nearest_segment_id)
#         print("Minimum distance:", min_distance, "meters")
#     else:
#         print("No line segment found")
