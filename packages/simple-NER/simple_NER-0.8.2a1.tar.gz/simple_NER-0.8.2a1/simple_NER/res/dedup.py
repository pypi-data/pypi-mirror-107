from os.path import  join, dirname
from os import listdir
import json
from pprint import pprint
from quebra_frases.list_utils import flatten


countries = join(dirname(__file__), "countries.json")
cities = join(dirname(__file__), "cities.json")

with open(countries) as f:
    country_data = json.load(f)
    capitals = {v["capital"]: {"country": v["country_code"],
                               "name": v["capital"],
                               "lat": str(v['latlng'][0]),
                               "lng": str(v['latlng'][1])}
                for v in country_data}
    #pprint(capitals)

with open(cities) as f:
    city_data = json.load(f)
    print(len(city_data))
    seen = [c for c in capitals] + ["England"]
    cities = list(capitals.values())
    dups = []
    for c in city_data:
        if c["name"] in seen:
            dups.append(c)
        else:
            print(c)
            cities.append(c)
        seen.append(c["name"])

    pprint(cities)
    print(len(cities))

cities_dedup = join(dirname(__file__), "cities.json")
with open(cities_dedup, "w") as f:
    json.dump(cities, f)