"""Чернетка / draft"""

from dozor_scraper import ALL_ROUTES_QUERY_STRINGS
print("ROUTE_NUMBERS = {")
print("    # keys - route id's from dozor")
print("    # values - route numbers")
print(*[f'    {val[11:]}: "{key}",'
        for key, val in ALL_ROUTES_QUERY_STRINGS.items()
        ], sep="\n")
print("}")
