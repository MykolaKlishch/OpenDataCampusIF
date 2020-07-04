"""transform data_for_each_vehicle.json from json to csv
UTC time converted to local time
"""

import json
import csv
from datetime import datetime, timezone


def utc_to_local(utc_dt_str):
    utc_dt = datetime.fromisoformat(utc_dt_str.replace("Z", ""))
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def main():
    with open(
            "data_for_each_vehicle.json", mode="rt", encoding="utf-8"
    ) as fh_json, open(
            file="data_for_each_vehicle.csv", mode="wt", encoding="utf-8",
            newline="") as fh_csv:
        data_for_each_vehicle = json.load(fh_json)
        fieldnames = ["StateNumber", "RouteNumber", "Timestamp",
                      "lat", "lng", "spd", "azi"]
        writer = csv.DictWriter(f=fh_csv, fieldnames=fieldnames)
        writer.writeheader()
        for gNb, vehicle_data in data_for_each_vehicle.items():
            for timestamp, geo_speed_data in vehicle_data["positions"].items():
                writer.writerow({
                    "StateNumber": gNb,
                    "RouteNumber": vehicle_data["route_number"],
                    "Timestamp": utc_to_local(timestamp),
                    "lat": geo_speed_data["loc"]["lat"],
                    "lng": geo_speed_data["loc"]["lng"],
                    "spd": geo_speed_data["spd"],
                    "azi": geo_speed_data["azi"],
                })


if __name__ == "__main__":
    main()



