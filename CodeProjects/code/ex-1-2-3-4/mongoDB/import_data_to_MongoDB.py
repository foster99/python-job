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

    RESTAURANTS_PATH = './data/restaurants_input.json'
    SEGMENTS_PATH = './data/segments_input.json'

    print("Droping all collections from DB ...")
    rdbm.drop_all_collections()
    print(" -> Succesfully dropped.\n")

    print("Importing data from JSON to Python ...")
    (restaurants, segments) = rdbm.import_restaurants_and_segments_from_file_to_dict(RESTAURANTS_PATH, SEGMENTS_PATH)
    print(" -> Succesfully imported.\n")
    
    print("Importing data from Python to MongoDB ...")
    rdbm.import_restaurants_and_segments_from_dict_to_db(restaurants, segments)
    print(" -> Succesfully imported.\n")


if __name__ == "__main__":
    main()
