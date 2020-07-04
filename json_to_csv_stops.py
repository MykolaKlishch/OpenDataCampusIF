"""transform data_for_each_vehicle.json from json to csv
UTC time converted to local time
"""

import json
import csv
from datetime import datetime, timezone


def main():
    with open(
            "routes_stops_data.json", mode="rt", encoding="utf-8"
    ) as fh_json, open(
            file="routes_stops_data.csv", mode="wt", encoding="utf-8",
            newline="") as fh_csv:
        routes_stops_json = json.load(fh_json)
        fieldnames = ["lat_ctr", "lng_ctr", "lat_pt", "lng_pt",
                      "StopName", "UsedByRoute"]
        writer = csv.DictWriter(f=fh_csv, fieldnames=fieldnames)
        writer.writeheader()
        for route in routes_stops_json["data"]:
            for stop in route["zns"]:
                writer.writerow({
                    "lat_ctr": stop["ctr"]["lat"],
                    "lng_ctr": stop["ctr"]["lng"],
                    "lat_pt": stop["pt"]["lat"],
                    "lng_pt": stop["pt"]["lng"],
                    "StopName": stop["nm"][1],
                    "UsedByRoute": route["sNm"]
                })


if __name__ == "__main__":
    main()



