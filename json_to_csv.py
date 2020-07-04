"""transform data_for_each_vehicle.json from json to csv"""

import json
import csv


data_for_each_vehicle = json.load(
    open("data_for_each_vehicle.json", mode="rt", encoding="utf-8-sig"))
fieldnames = ["StateNumber", "RouteNumber", "Timestamp",
              "lat", "lng", "spd", "azi"]
writer = csv.DictWriter(f=open(
    file="data_for_each_vehicle.csv", mode="wt", encoding="utf-8", newline=""
), fieldnames=fieldnames)
writer.writeheader()
for gNb, vehicle_data in data_for_each_vehicle.items():
    for timestamp, geo_speed_data in vehicle_data["positions"].items():
        writer.writerow({
            "StateNumber": gNb,
            "RouteNumber": vehicle_data["route_number"],
            "Timestamp": timestamp,
            "lat": geo_speed_data["loc"]["lat"],
            "lng": geo_speed_data["loc"]["lng"],
            "spd": geo_speed_data["spd"],
            "azi": geo_speed_data["azi"],
        })


