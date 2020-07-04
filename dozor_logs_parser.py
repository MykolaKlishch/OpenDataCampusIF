"""Attention! Timestamps are in UTC!"""

import os
import json
import datetime
from math import radians, cos, sin, asin, sqrt


ROUTE_NUMBERS = {
    # keys - route id's from dozor
    # values - route numbers
    918: "21",
    843: "22",
    919: "23",
    920: "24",
    921: "25",
    936: "26",
    922: "26А",
    1554: "27",
    849: "28",
    929: "29",
    924: "30",
    934: "31",
    861: "32",
    937: "33",
    847: "34",
    932: "35",
    930: "36",
    856: "37",
    942: "38",
    935: "39",
    938: "40",
    1711: "40К",
    1608: "41К",
    848: "42",
    943: "43",
    939: "44",
    1794: "45",
    945: "48",
    946: "49",
    2186: "53",
    2187: "54",
    1660: "55",
    2181: "56",
    1740: "47-47(Бер)",
    893: "2",
    1531: "3",
    896: "4",
    1854: "5",
    897: "6",
    898: "7",
    903: "10",
    1310: "С1",
    1309: "С2",
    1314: "С3",
    1315: "С4",
    1312: "С5",
    1311: "С6",
    1313: "С7",
    864: "С8",
    1537: "С9",
    1538: "С10",
}


def to_be_discarded(entry):
    """Not all entries contain vehicles positions data"""
    return (
        "response" not in entry.keys()
        or "content" not in entry["response"].keys()
        or "text" not in entry["response"]["content"].keys()
        # non-json data are discarded by the following condition:
        or entry["response"]["content"]["text"][0] not in "{["
        # bus stops data are discarded by the following condition:
        or "rId" not in entry["response"]["content"]["text"]
    )


def get_vehicles_positions_from_log(log_abs_filename):
    file_handle = open(log_abs_filename, "rt", encoding='utf-8')
    log_json = json.loads(file_handle.read())
    vehicles_positions = {}
    for entry in log_json["log"]["entries"]:
        if to_be_discarded(entry):
            continue
        vehicles_positions[entry["startedDateTime"]] = \
            json.loads(entry["response"]["content"]["text"])
    return vehicles_positions


def validate_vehicles_positions(vehicles_positions):
    for all_routes_record in vehicles_positions.values():
        for single_route_record in all_routes_record['data']:
            assert "rId" in single_route_record.keys()
            assert "dvs" in single_route_record.keys()
            for single_vehicle_record in single_route_record["dvs"]:
                assert "id" in single_vehicle_record.keys()
                assert "loc" in single_vehicle_record.keys()
                assert "spd" in single_vehicle_record.keys()
                assert "azi" in single_vehicle_record.keys()
                assert "gNb" in single_vehicle_record.keys()


def get_filenames_in_folder(folder_name):
    path = os.path.join(os.getcwd(), folder_name)
    filenames = tuple(os.walk(path))[0][2]
    abs_filenames = [os.path.join(path, filename) for filename in filenames]
    return abs_filenames


def update_data_for_each_vehicle(vehicles_positions, data_for_each_vehicle):
    """
    input data: all vehicles for specific time point(s)
    output data: all time points for specific vehicle(s)
    """
    for all_routes_record in vehicles_positions.items():
        datetime = all_routes_record[0]
        for single_route_record in all_routes_record[1]['data']:
            if "dvs" in single_route_record.keys():
                for single_vehicle_record in single_route_record["dvs"]:
                    vehicle_registration_number = \
                        single_vehicle_record["gNb"].replace(" ", "")
                    single_vehicle_record_filtered = {
                        key: value
                        for key, value in single_vehicle_record.items()
                        if key in ("loc", "spd", "azi")
                        # BTW, what are "dis" and "rad"?
                    }
                    if (vehicle_registration_number
                            not in data_for_each_vehicle.keys()):
                        data_for_each_vehicle[vehicle_registration_number] = {
                            "vehicle_id_dozor": single_vehicle_record["id"],
                            "route_id_dozor": single_route_record["rId"],
                            "route_number": ROUTE_NUMBERS[
                                single_route_record["rId"]
                            ],
                            "positions": {
                                datetime: single_vehicle_record_filtered,
                            }
                        }
                    elif (vehicle_registration_number
                            in data_for_each_vehicle.keys()):
                        data_for_each_vehicle[
                            vehicle_registration_number][
                            "positions"][datetime] = \
                            single_vehicle_record_filtered
    return data_for_each_vehicle


def haversine(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    source: https://gist.github.com/DeanThompson/d5d745eca4e9023c6501
    """
    # convert decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])

    # haversine formula
    d_lat = lat2 - lat1
    d_lng = lng2 - lng1
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def calculate_average_speed(positions):
    """Calculates average speed based on time and geospatial data"""
    time_list_str = sorted(positions)
    time_list_datetime = list(
        datetime.datetime.fromisoformat(timestamp.replace("Z", ""))
        for timestamp in time_list_str)
    total_d = 0  # total distance in km
    for num, timestamp in enumerate(time_list_str):
        lat = positions[time_list_str[num]]["loc"]["lat"]
        lng = positions[time_list_str[num]]["loc"]["lng"]
        if num > 0:
            delta_d = haversine(prev_lat, prev_lng, lat, lng)
            total_d += delta_d
        prev_lat = lat
        prev_lng = lng
    seconds_in_hour = 3600
    total_t = (time_list_datetime[-1] - time_list_datetime[0]
               ).total_seconds() / seconds_in_hour
    return total_d / total_t


def aggregate_speed_from_dozor(positions):
    """
    Disclaimer: in general, average speed is NOT just an arithmetic average
    of all speed values. Average speed is total_distance/total_time
    (this calculation is implemented in calculate_average_speed(positions))
    However, in this case speed measurements were
    taken at roughly the same intervals (approx. 10 seconds). Therefore
    we can assume that this is a degenerate case and the average speed
    can be approximated as an average of all these speed measurements
    The purpose of this function is to provide alternative speed
    calculation for comparison.
    """
    speed_measurements = [
        position_record["spd"]
        for position_record in positions.values()
    ]
    return sum(speed_measurements) / len(speed_measurements)


def dump_json(data_for_each_vehicle):
    with open("data_for_each_vehicle.json", "wt",
              encoding="utf-8") as file_handle:
        json.dump(obj=data_for_each_vehicle, fp=file_handle,
                  ensure_ascii=False, separators=(',', ':'))


def dump_flat_file(data_for_each_vehicle):
    """
    This file contains only selected data
    The data in dump file are NOT the same as
    the data data_for_each_vehicle.json
    """
    with open("data_for_each_vehicle.txt",
              mode="wt", encoding="utf-8") as file_handle:
        headers_en = ("RouteNumber\tStateNumber\t"
                      "AvgSpeedDozor, km/h\t"
                      "AvgSpeedRecalculated, km/h\n")
        headers_uk = ("Номер маршруту\tДержавний номер\t"
                      "Середня швидкість (вимір. dozor), км/год\t"
                      "Середня швидкість (перерахована), км/год\n")
        file_handle.write(headers_en)
        file_handle.write(headers_uk)
        for gNb, vehicle_data in data_for_each_vehicle.items():
            file_handle.write(
                f"{vehicle_data['route_number']}"
                f"\t{gNb}"
                f"\t{vehicle_data['avg_spd']}"
                f"\t{vehicle_data['avg_spd_recalc']}\n".replace(".", ",")
            )


def main():
    dozor_logs_abs_filenames = get_filenames_in_folder("dozor_logs")
    data_for_each_vehicle = dict()
    for num, abs_filename in enumerate(dozor_logs_abs_filenames):
        print(f"Parsing log {num + 1} of "
              f"{len(dozor_logs_abs_filenames)}"
              f": {abs_filename}"
              )
        vehicles_positions = get_vehicles_positions_from_log(abs_filename)
        validate_vehicles_positions(vehicles_positions)
        data_for_each_vehicle = update_data_for_each_vehicle(
            vehicles_positions, data_for_each_vehicle)
    data_for_each_vehicle_w_speed = {}
    for gNb, vehicle_data in data_for_each_vehicle.items():
        vehicle_data["avg_spd"] = aggregate_speed_from_dozor(
            vehicle_data["positions"])
        vehicle_data["avg_spd_recalc"] = calculate_average_speed(
            vehicle_data["positions"])
        data_for_each_vehicle_w_speed.update({
            gNb: vehicle_data
        })
    data_for_each_vehicle = data_for_each_vehicle_w_speed
    dump_json(data_for_each_vehicle)
    dump_flat_file(data_for_each_vehicle)


if __name__ == "__main__":
    main()
