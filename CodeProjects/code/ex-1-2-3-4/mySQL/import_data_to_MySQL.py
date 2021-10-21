# add to path, the parent dir
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Restaurants_db_manager as rdbm

def main():

    # Database connection info
    DB_URL  = 'sfexam.delectame.develop'
    DB_NAME = 'exam_dev'
    DB_USER = 'root'
    DB_PASS = 'delectaRoot1234!'

    # Table definition
    TABLES = {}
    TABLES['Segment'] = (
        "CREATE TABLE Segment ("
        "  `name` VARCHAR(255) NOT NULL,"
        "  `size` INTEGER NOT NULL,"
        "  `uidentifier` VARCHAR(255) PRIMARY KEY,"
        "  `average_popularity_rate` DOUBLE,"
        "  `average_satisfaction_rate` DOUBLE,"
        "  `average_price` DOUBLE,"
        "  `total_reviews` INTEGER"
        ")")
    TABLES['Restaurant'] = (
        "CREATE TABLE `Restaurant` ("
        "  `name` VARCHAR(255) NOT NULL,"
        "  `street_address` VARCHAR(255),"
        "  `uidentifier` VARCHAR(255) PRIMARY KEY,"
        "  `latitude` DOUBLE NOT NULL,"
        "  `longitude` DOUBLE NOT NULL,"
        "  `city_name` VARCHAR(255) NOT NULL,"
        "  `popularity_rate` DOUBLE NOT NULL,"
        "  `satisfaction_rate` DOUBLE NULL,"
        "  `total_reviews` INTEGER NOT NULL,"
        "  `average_price` DOUBLE NOT NULL"
        ")")
    TABLES['Restaurant_Segment_Association'] = (
        "CREATE TABLE `Restaurant_Segment_Association` ("
        "  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "  `restaurantUID` VARCHAR(255),"
        "  `segmentUID` VARCHAR(255),"
        "  FOREIGN KEY (`restaurantUID`) REFERENCES `Restaurant` (`uidentifier`) ON DELETE CASCADE,"
        "  FOREIGN KEY (`segmentUID`) REFERENCES `Segment` (`uidentifier`) ON DELETE CASCADE,"
        "  UNIQUE KEY (`segmentUID`,`restaurantUID`)"
        ")")

    # Data paths
    RESTAURANTS_PATH = './data/restaurants_input.json'
    SEGMENTS_PATH = './data/segments_input.json'
    




    # Primer Apartado

    dbm = rdbm.Restaurants_db_manager()
    dbm.connect(DB_URL, DB_NAME, DB_USER, DB_PASS)
    dbm.select_database(DB_NAME)
    dbm.drop_all_tables()
    dbm.load_tables(TABLES)
    dbm.import_restaurants_to_mySqlDB(RESTAURANTS_PATH)
    dbm.import_segments_to_mySqlDB(SEGMENTS_PATH)






    # Segundo Apartado

    params1 = {
        "popularity_rate": {"gt": 8},
        "city_name": {"eq": 'Madrid'}
    }
    result1 = dbm.query_restaurants(params1)
    print(result1)


    params2 = {
        "popularity_rate": {"lt": 0},
        "city_name": {"eq": 'Madrid'}
    }
    result2 = dbm.query_restaurants(params2)
    print(result2)

    params3 = {
        "street_address": {"eq": None},
        "satisfaction_rate": {"gt": 9},
    }
    result3 = dbm.query_restaurants(params3)
    print(result3)





    # Tercer Apartado

    data = dbm.export_all_data()
    file = open("./data/exported_data.json","w")
    file.write(data)
    file.close()

    dbm.disconnect()

    
if __name__ == "__main__":
    main()
