# add to path, the parent dir
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Restaurants_MongoDB_manager import Restaurants_MongoDB_manager
from pprint import pprint
import urllib.parse

USERNAME = urllib.parse.quote_plus("delecta_root")
PASSWORD = urllib.parse.quote_plus("delectaRoot1234!")
DB_IP = "192.168.70.70"
DB_PORT = "27017"
DB_NAME = "delectaDatabase"

rdbm = Restaurants_MongoDB_manager( url=DB_IP, 
                                        port=DB_PORT, 
                                        user=USERNAME, 
                                        password=PASSWORD,
                                        db_name=DB_NAME)

def main():

    params1 = {
        "popularity_rate": {"gt": 8},
        "city_name": {"eq": 'Madrid'}
    }
    print("QUERY 1: Querying over Restaurants collection with params:")
    pprint(params1)
    print("Result:")

    for restaurant in rdbm.query_restaurants(params1):
        pprint(restaurant)
    
    
    params2 = {
        "popularity_rate": {"lt": 0},
        "city_name": {"eq": 'Madrid', "eq1": 'Madrid'}
    }
    print("QUERY 2: Querying over Restaurants collection with params:")
    pprint(params2)
    print("Result:")

    for restaurant in rdbm.query_restaurants(params2):
        pprint(restaurant)
    

    params3 = {
        "street_address": {"eq": None},
        "satisfaction_rate": {"gt": 9},
    }
    print("QUERY 3: Querying over Restaurants collection with params:")
    pprint(params3)
    print("Result:")

    for restaurant in rdbm.query_restaurants(params3):
        pprint(restaurant)


if __name__ == "__main__":
    main()
