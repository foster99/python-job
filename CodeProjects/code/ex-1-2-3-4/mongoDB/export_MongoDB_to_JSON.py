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

    PATH = "./data/exported_data_mongoDB.json"
    
    print("Exporting data to file ...")
    rdbm.export_all_data_to_file(PATH)
    print("Succesfully exported!")

if __name__ == "__main__":
    main()
