"""Чернетка / Draft"""

from urllib.request import urlretrieve
from dozor_scraper import BASE_URL, ALL_ROUTES_QUERY_STRINGS, ROUTE_NUMBERS

for route_number in ROUTE_NUMBERS:
    # print(f"{route_number:<11} "
    #       f"{BASE_URL + ALL_ROUTES_QUERY_STRINGS[route_number]}")
    url = BASE_URL + ALL_ROUTES_QUERY_STRINGS[route_number]
    urlretrieve(url, f"{route_number}.txt")

