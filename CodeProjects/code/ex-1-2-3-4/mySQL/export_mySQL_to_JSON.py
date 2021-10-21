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
        

    data = dbm.export_all_data()
    file = open("./data/exported_data_mySQL.json","w")
    file.write(data)
    file.close()
    dbm.disconnect()

if __name__ == "__main__":
    main()