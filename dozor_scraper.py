"""Performs the scraping of JSON files from city.dozor.tech
Ivano Frankivsk only (hardcoded)

BASE_URL:
protocol + hostname

QUERY_STRINGS:
    keys - route numbers
    values - filename + query string
        query strings are different for eac
        param t=2 - city (Ivano-Frankivsk) (?)
        param p - unique for each route
"""

import json
import requests

BASE_URL = "https://city.dozor.tech/"  # protocol + hostname

BUSES_QUERY_STRINGS = {
    "21": "data?t=2&p=918",
    "22": "data?t=2&p=843",
    "23": "data?t=2&p=919",
    "24": "data?t=2&p=920",
    "25": "data?t=2&p=921",
    "26": "data?t=2&p=936",
    "26А": "data?t=2&p=922",
    "27": "data?t=2&p=1554",
    "28": "data?t=2&p=849",
    "29": "data?t=2&p=929",
    "30": "data?t=2&p=924",
    "31": "data?t=2&p=934",
    "32": "data?t=2&p=861",
    "33": "data?t=2&p=937",
    "34": "data?t=2&p=847",
    "35": "data?t=2&p=932",
    "36": "data?t=2&p=930",
    "37": "data?t=2&p=856",
    "38": "data?t=2&p=942",
    "39": "data?t=2&p=935",
    "40": "data?t=2&p=938",
    "40К": "data?t=2&p=1711",
    "41К": "data?t=2&p=1608",
    "42": "data?t=2&p=848",
    "43": "data?t=2&p=943",
    "44": "data?t=2&p=939",
    "45": "data?t=2&p=1794",
    "48": "data?t=2&p=945",
    "49": "data?t=2&p=946",
    "53": "data?t=2&p=2186",
    "54": "data?t=2&p=2187",
    "55": "data?t=2&p=1660",
    "56": "data?t=2&p=2181",
    "47-47(Бер)": "data?t=2&p=1740",
    # "47/47(Бер)" renamed because / is
    # illegal char for file names
}
TROLLEYS_QUERY_STRINGS = {
    "2": "data?t=2&p=893",
    "3": "data?t=2&p=1531",
    "4": "data?t=2&p=896",
    "5": "data?t=2&p=1854",
    "6": "data?t=2&p=897",
    "7": "data?t=2&p=898",
    "10": "data?t=2&p=903",
}

COTTAGE_BUSES_QUERY_STRINGS = {
    "С1": "data?t=2&p=1310",
    "С2": "data?t=2&p=1309",
    "С3": "data?t=2&p=1314",
    "С4": "data?t=2&p=1315",
    "С5": "data?t=2&p=1312",
    "С6": "data?t=2&p=1311",
    "С7": "data?t=2&p=1313",
    "С8": "data?t=2&p=864",
    "С9": "data?t=2&p=1537",
    "С10": "data?t=2&p=1538",
}
