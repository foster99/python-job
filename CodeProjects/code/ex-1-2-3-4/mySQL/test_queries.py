# add to path, the parent dir
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Restaurants_db_manager as rdbm


# Database connection info
DB_URL  = '192.168.70.70'
DB_NAME = 'exam_dev'
DB_USER = 'root'
DB_PASS = 'delectaRoot1234!'
    
# Connect to mySQL DB
dbm = rdbm.Restaurants_db_manager()
dbm.connect(DB_URL, DB_NAME, DB_USER, DB_PASS)
dbm.select_database(DB_NAME)


def main():

    print("\n\n\n")
    
    params1 = {
        "popularity_rate": {"gt": 8},
        "city_name": {"eq": 'Madrid'}
    }
    print(f"QUERY 1 with params: \n {params1}")
    result1 = dbm.query_restaurants(params1)
    print(f"Result:\n{result1}")

    print("\n\n\n")

    params2 = {
        "popularity_rate": {"lt": 0},
        "city_name": {"eq": 'Madrid'}
    }
    print(f"QUERY 2 with params: \n {params2}")
    result2 = dbm.query_restaurants(params2)
    print(f"Result:\n{result2}")

    print("\n\n\n")

    params3 = {
        "street_address": {"eq": None},
        "satisfaction_rate": {"gt": 9},
    }
    print(f"QUERY 3 with params: \n {params3}")
    result3 = dbm.query_restaurants(params3)
    print(f"Result:\n{result3}")

    dbm.disconnect()

if __name__ == "__main__":
    main()
