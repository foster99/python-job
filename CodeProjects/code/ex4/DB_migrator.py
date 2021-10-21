import Restaurants_db_manager as mySQL_manager
import Restaurants_MongoDB_manager as mongo_manager


def clear_mongoDB(MongoDB_credentials) -> bool:
    
    db = mongo_manager.Restaurants_MongoDB_manager( url=MongoDB_credentials['DB_URL'],
                                                    port=MongoDB_credentials['DB_PORT'],
                                                    user=MongoDB_credentials['DB_USER'],
                                                    password=MongoDB_credentials['DB_PASS'],
                                                    db_name=MongoDB_credentials['DB_NAME'])
    
    return db.drop_all_collections()
    

def clear_mySQL(MySQL_credentials) -> bool:

    db = mySQL_manager.Restaurants_db_manager()
    db.connect( DB_URL=MySQL_credentials['DB_URL'],
                DB_USER=MySQL_credentials['DB_USER'],
                DB_PASS=MySQL_credentials['DB_PASS'],
                DB_NAME=MySQL_credentials['DB_NAME'])

    return db.drop_all_tables()

    
def migrate_from_mongoDB_to_mySQL(MongoDB_credentials, MySQL_credentials) -> bool:

    # download from mongo
    mongo = mongo_manager.Restaurants_MongoDB_manager(  url=MongoDB_credentials['DB_URL'],
                                                        port=MongoDB_credentials['DB_PORT'],
                                                        user=MongoDB_credentials['DB_USER'],
                                                        password=MongoDB_credentials['DB_PASS'],
                                                        db_name=MongoDB_credentials['DB_NAME'])


    restaurant_list = mongo.get_list_of_all_restaurants_without_segment_data()
    restaurant_columnNames = list(restaurant_list[0].keys())
    restaurants = [list(rest.values()) for rest in restaurant_list]
    
    segment_list = mongo.get_list_of_all_segments()
    segment_columnNames = list(segment_list[0].keys())
    segments = [list(rest.values()) for rest in segment_list]

    rs_association = []
    rs_columnNames = ['restaurantUID', 'segmentUID']
    for segment in segment_list:
        segmentUID = segment['uidentifier']
        restaurants_of_segment = mongo.get_restaurants_uids_of_segment(segmentUID)
        rs_association += [[restaurant['uidentifier'], segmentUID] for restaurant in restaurants_of_segment]
            
    # migrate to mySQL

    mySql = mySQL_manager.Restaurants_db_manager()
    mySql.connect(  DB_URL=MySQL_credentials['DB_URL'],
                    DB_USER=MySQL_credentials['DB_USER'],
                    DB_PASS=MySQL_credentials['DB_PASS'],
                    DB_NAME=MySQL_credentials['DB_NAME'])

    # Create tables
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
    mySql.load_tables(TABLES)

    # Insert Values on tables
    if mySql.insert_into_restaurants(restaurant_columnNames, restaurants):
        if mySql.insert_into_segmetns(segment_columnNames, segments):
            if mySql.insert_into_rs_association(rs_columnNames, rs_association):
                return True

    return False


def migrate_from_mySQL_to_mongoDB(MySQL_credentials, MongoDB_credentials) -> bool:

    # download from mySQL

    mySql = mySQL_manager.Restaurants_db_manager()
    mySql.connect(  DB_URL=MySQL_credentials['DB_URL'],
                    DB_USER=MySQL_credentials['DB_USER'],
                    DB_PASS=MySQL_credentials['DB_PASS'],
                    DB_NAME=MySQL_credentials['DB_NAME'])


    segment_list = mySql.get_all_segments(dictionary=True)
    if segment_list is None:
        print("Could not download the Segment list from MySQL DB.")
        return False

    restaurant_list = mySql.get_all_restaurants_joined_to_segments(dictionary=True)
    if restaurant_list is None:
        print("Could not download the Restaurant list from MySQL DB.")
        return False
    
    restaurants = {}

    for restaurant in restaurant_list:
        
        if restaurant['uidentifier'] not in restaurants:
            
            restaurants[restaurant['uidentifier']] = {
                'name'              : restaurant['name'],
                'street_address'    : restaurant['street_address'],
                'uidentifier'       : restaurant['uidentifier'],
                'latitude'          : restaurant['latitude'],
                'longitude'         : restaurant['longitude'],
                'city_name'         : restaurant['city_name'],
                'popularity_rate'   : restaurant['popularity_rate'],
                'satisfaction_rate' : restaurant['satisfaction_rate'],
                'total_reviews'     : restaurant['total_reviews'],
                'average_price'     : restaurant['average_price'],
                'segment_uids'          : []
            }
        
        if restaurant['segmentUID'] is not None:
            restaurants[restaurant['uidentifier']]['segment_uids'].append(restaurant['segmentUID'])
        

    # migrate to mongo

    mongo = mongo_manager.Restaurants_MongoDB_manager(  url=MongoDB_credentials['DB_URL'],
                                                        port=MongoDB_credentials['DB_PORT'],
                                                        user=MongoDB_credentials['DB_USER'],
                                                        password=MongoDB_credentials['DB_PASS'],
                                                        db_name=MongoDB_credentials['DB_NAME'])

    if not mongo.insert_many_restaurants(list(restaurants.values())):
        print("Could not insert the Restaurant list in mongoDB.")
        return False
    
    if not mongo.insert_many_segments(segment_list):
        print("Could not insert the Segment list in mongoDB.")
        return False
    
    return True


