from Restaurants_MongoDB_manager import Restaurants_MongoDB_manager
from pprint import pprint
import urllib.parse

USERNAME = urllib.parse.quote_plus("delecta_root")
PASSWORD = urllib.parse.quote_plus("delectaRoot1234!")
DB_IP = "192.168.70.70"
DB_PORT = "27017"
DB_NAME = "delectaDatabase"
RESTAURANTS_PATH = './data/restaurants_input.json'
SEGMENTS_PATH = './data/segments_input.json'


def main():

    rdbm = Restaurants_MongoDB_manager( url=DB_IP, 
                                        port=DB_PORT, 
                                        user=USERNAME, 
                                        password=PASSWORD,
                                        db_name=DB_NAME)
    
    
    # Part 1: Load data from files to DB
    print("###############   PART 1   ###############")

    print("Droping all collections from DB ...")
    rdbm.drop_all_collections()
    print(" -> Succesfully dropped.\n")

    print("Importing data from JSON to Python ...")
    (restaurants, segments) = rdbm.import_restaurants_and_segments_from_file_to_dict(RESTAURANTS_PATH, SEGMENTS_PATH)
    print(" -> Succesfully imported.\n")
    
    print("Importing data from Python to MongoDB ...")
    rdbm.import_restaurants_and_segments_from_dict_to_db(restaurants, segments)
    print(" -> Succesfully imported.\n")



    # Part 2: Query over restaurants
    print("###############   PART 2   ###############")


    params1 = {
        "popularity_rate": {"gt": 8},
        "city_name": {"eq": 'Madrid'}
    }
    print("Querying over Restaurants collection with params:")
    pprint(params1)
    print("Result:")

    for restaurant in rdbm.query_restaurants(params1):
        pprint(restaurant)
    
    
    params2 = {
        "popularity_rate": {"lt": 0},
        "city_name": {"eq": 'Madrid', "eq1": 'Madrid'}
    }
    print("Querying over Restaurants collection with params:")
    pprint(params2)
    print("Result:")

    for restaurant in rdbm.query_restaurants(params2):
        pprint(restaurant)
    

    params3 = {
        "street_address": {"eq": None},
        "satisfaction_rate": {"gt": 9},
    }
    print("Querying over Restaurants collection with params:")
    pprint(params3)
    print("Result:")

    for restaurant in rdbm.query_restaurants(params3):
        pprint(restaurant)




    # Part 3: Export all data to file
    print("###############   PART 3   ###############")

    print("Exporting data to file ...")
    path = "./data/exported_data_mongoDB.json"
    rdbm.export_all_data_to_file(path)
    print("Succesfully exported!")

    print("##########################################")
    print("DONE")

if __name__ == "__main__":
    main()