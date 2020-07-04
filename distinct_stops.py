"""
stop records with the same coodrinates
will be reduced to a single record
"""

import json
import csv
from datetime import datetime, timezone


def main():
    with open(
            "routes_stops_data.csv", mode="rt", encoding="utf-8"
    ) as fh_csv_in, open(
            file="distinct_stops_data.csv", mode="wt", encoding="utf-8",
            newline="") as fh_csv_out:
        distinct_stops = dict()
        reader = csv.DictReader(f=fh_csv_in)
        for row in reader:
            key = (row["lat_ctr"], row["lng_ctr"],
                   row["lat_pt"], row["lng_pt"])
            val = row["StopName"]
            distinct_stops[key] = val
        writer = csv.writer(fh_csv_out)
        writer.writerow(["lat_ctr", "lng_ctr", "lat_pt", "lng_pt",
                         "StopName"])
        for coordinates, name in distinct_stops.items():
            writer.writerow(list(coordinates) + [name])


if __name__ == "__main__":
    main()



