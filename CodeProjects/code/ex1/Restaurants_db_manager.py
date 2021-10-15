import MySQL_connector as MySQL
import json

class Restaurants_db_manager:

    def __init__(self):
        self.mySqlDB = MySQL.MySQL_connector()

    def connect(self, DB_URL, DB_NAME, DB_USER, DB_PASS):
        self.mySqlDB.connect_to_database(DB_URL, DB_NAME, DB_USER, DB_PASS)

    def disconnect(self):
        self.mySqlDB.close_database_connection()

    def select_database(self, DB_NAME):
        self.mySqlDB.select_database(DB_NAME, create_if_missing=True)

    def load_tables(self, TABLES):
        self.mySqlDB.add_tables_to_database(TABLES)

    def drop_all_tables(self):
        self.mySqlDB.drop_table("Restaurant_Segment_Association")
        self.mySqlDB.drop_table("Restaurant")
        self.mySqlDB.drop_table("Segment")

    def import_restaurants_to_mySqlDB(self, path):

        with open(path) as json_restaurant_file:

            data = json.load(json_restaurant_file)

            print("Importing Restaurants to DB:")

            values = []
            restaurantUIDs = set()

            for restaurant in data:

                # Use restaurant uniquenes constraint to avoid PRIMARY KEY violation
                uidentifier = "\'" + str(restaurant['uidentifier']).replace('\'','\\\'').replace('\\\\', '\\') + "\'" if restaurant['uidentifier'] != None else "NULL"
                
                if uidentifier in restaurantUIDs:
                    continue
                restaurantUIDs.add(uidentifier)

                name = "\'" + str(restaurant['name']).replace('\'','\\\'').replace('\\\\', '\\') + "\'" if restaurant['name'] != None else "NULL"
                street_address = "\'" + str(restaurant['street_address']).replace('\'','\\\'').replace('\\\\', '\\') + "\'" if restaurant['street_address'] != None else "NULL"
                latitude = float(restaurant['latitude']) if restaurant['latitude'] != None else "NULL"
                longitude = float(restaurant['longitude']) if restaurant['longitude'] != None else "NULL"
                city_name = "\'" + str(restaurant['city_name']).replace('\'','\\\'').replace('\\\\', '\\') + "\'" if restaurant['city_name'] != None else "NULL"
                popularity_rate = float(restaurant['popularity_rate']) if restaurant['popularity_rate'] != None else "NULL"
                satisfaction_rate = float(restaurant['satisfaction_rate']) if restaurant['satisfaction_rate'] != None else "NULL"
                total_reviews = int(restaurant['total_reviews']) if restaurant['total_reviews'] != None else "NULL"
                average_price = float(restaurant['average_price']) if restaurant['average_price'] != None else "NULL"

                values.append([ name,
                                street_address,
                                uidentifier,
                                latitude,
                                longitude,
                                city_name,
                                popularity_rate,
                                satisfaction_rate,
                                total_reviews,
                                average_price])

            column_names = ["name",
                            "street_address",
                            "uidentifier",
                            "latitude",
                            "longitude",
                            "city_name",
                            "popularity_rate",
                            "satisfaction_rate",
                            "total_reviews",
                            "average_price"]

            self.mySqlDB.insertInTable("Restaurant", column_names, values)

    def import_segments_to_mySqlDB(self, path):

        with open(path) as json_segments_file:

            data = json.load(json_segments_file)
            

            # Import Segment basic data
            column_names = ["name","size","uidentifier"]
            segmentUIDs = set()
            values = []

            for segment_dict in data:

                # Use segment uniquenes constraint to avoid PRIMARY KEY violation
                uidentifier = "\'" + str(segment_dict['uidentifier']).replace('\'','\\\'').replace('\\\\', '\\') + "\'" if segment_dict['uidentifier'] != None else "NULL"
                
                if uidentifier in segmentUIDs: continue
                segmentUIDs.add(uidentifier)
                
                name = "\'" + str(segment_dict['name']).replace('\'','\\\'').replace('\\\\', '\\') + "\'" if segment_dict['name'] != None else "NULL"
                size = int(segment_dict['size'])

                values.append([name, size, uidentifier])

            self.mySqlDB.insertInTable("Segment", column_names, values)
            

            # Import Segment-Restaurant relation
            column_names = ["segmentUID","restaurantUID"]
            values = []
            segmentUIDs = set()

            for segment_dict in data:

                # Use segment uniquenes constraint to avoid PRIMARY KEY violation
                segmentUID = "\'" + str(segment_dict['uidentifier']).replace('\'','\\\'').replace('\\\\', '\\') + "\'" if segment_dict['uidentifier'] != None else "NULL"
                
                if segmentUID in segmentUIDs: continue
                segmentUIDs.add(segmentUID)

                restaurantsUIDs = set()
                for restaurant in segment_dict['restaurants']:
                    
                    restaurantUID = "\'" + str(restaurant).replace('\'','\\\'').replace('\\\\', '\\') + "\'" if restaurant != None else "NULL"

                    # Use restaurant uniquenes constraint to avoid PRIMARY KEY violation
                    if restaurantUID in restaurantsUIDs: continue
                    restaurantsUIDs.add(restaurantUID)

                    values.append([segmentUID, restaurantUID])

            self.mySqlDB.insertInTable("Restaurant_Segment_Association", column_names, values)


            # Compute Segment Derived data

            avgPopularityQuery = (  "SELECT AVG(R.popularity_rate)\n"
                                    "FROM Segment S\n"
                                    "INNER JOIN Restaurant_Segment_Association RS ON S.uidentifier = RS.segmentUID\n"
                                    "INNER JOIN Restaurant R ON RS.restaurantUID = R.uidentifier\n"
                                    "WHERE S.uidentifier = target.uidentifier")

            avgSatisfactionQuery = (  "SELECT AVG(R.satisfaction_rate)\n"
                                    "FROM Segment S\n"
                                    "INNER JOIN Restaurant_Segment_Association RS ON S.uidentifier = RS.segmentUID\n"
                                    "INNER JOIN Restaurant R ON RS.restaurantUID = R.uidentifier\n"
                                    "WHERE S.uidentifier = target.uidentifier")

            avgPriceQuery = (  "SELECT AVG(R.average_price)\n"
                                    "FROM Segment S\n"
                                    "INNER JOIN Restaurant_Segment_Association RS ON S.uidentifier = RS.segmentUID\n"
                                    "INNER JOIN Restaurant R ON RS.restaurantUID = R.uidentifier\n"
                                    "WHERE S.uidentifier = target.uidentifier")
            
            totalReviewsQuery = (  "SELECT SUM(R.total_reviews)\n"
                                    "FROM Segment S\n"
                                    "INNER JOIN Restaurant_Segment_Association RS ON S.uidentifier = RS.segmentUID\n"
                                    "INNER JOIN Restaurant R ON RS.restaurantUID = R.uidentifier\n"
                                    "WHERE S.uidentifier = target.uidentifier")

            self.mySqlDB.set_derived_value('Segment', 'avgPopularity', avgPopularityQuery, table_alias='target')
            self.mySqlDB.set_derived_value('Segment', 'avgSatisfaction', avgSatisfactionQuery, table_alias='target')
            self.mySqlDB.set_derived_value('Segment', 'avgPrice', avgPriceQuery, table_alias='target')
            self.mySqlDB.set_derived_value('Segment', 'totalReviews', totalReviewsQuery, table_alias='target')

    def _get_operator_symbol(self, op, null_is_involved) -> str:

        if op == "gt" : 
            return ">"
        if op == "lt" :
            return "<"
        if op == "ge" : 
            return ">="
        if op == "le" :
            return "<="
        if op == "eq" :
            if null_is_involved:
                return "IS"
            else:
                return "="
        if op == "ne" :
            if null_is_involved:
                return "IS NOT"
            else:
                return "<>"
        return None

    def _format_value(self, value) -> str:

        # null
        if value is None: return "NULL"

        # numeric
        try:
            return_value = float(value)

            if str(return_value).indexOf('.') == -1:    # int
                return str(int(value))

            else:                                       # float
                return str(return_value)
        except:
            pass
        
        # boolean
        if str(value) == "True" or str(value) == "False":
            return str(value)

        # string
        return f"\'{str(value)}\'"

    def query_restaurants(self, params):

        where_statement = ""

        for attribute in params:
            for operator in params[attribute]:

                value = params[attribute][operator]

                if (len(where_statement) > 0): where_statement += " AND "
                
                formated_value = self._format_value(value)

                symbol_operator = self._get_operator_symbol(operator, null_is_involved=(value is None))

                where_statement += f"{attribute} {symbol_operator} {formated_value}"

        query = f"SELECT * FROM Restaurant R WHERE {where_statement};"
        return self.mySqlDB.consultant_query(query)

    def get_all_segments(self):

        query = f"SELECT S.uidentifier, S.name, S.size FROM Segment S;"

        list_of_segments = self.mySqlDB.raw_consultant_query(query)

        for segment in list_of_segments:
            segmentUID, name, size = segment
            segments[segmentUID] = (name, size, segmentUID, {})

        return f"{type(text)} \n \n {text}"

    def export_all_data(self) -> str:
        
        # Get and store all the restaurants
        restaurants = {}

        list_of_restaurants = self.mySqlDB.raw_consultant_query(
            f"SELECT name, street_address, latitude, longitude, city_name, popularity_rate,\
            satisfaction_rate, total_reviews, uidentifier, average_price  FROM Restaurant;")

        for restaurant in list_of_restaurants:
            name, street_address, latitude, longitude, city_name, popularity_rate,\
            satisfaction_rate, total_reviews, uidentifier, average_price = restaurant

            restaurants[uidentifier] = {
                "name" : name,
                "street_address" : street_address,
                "latitude" : latitude,
                "longitude" : longitude,
                "city_name" : city_name,
                "popularity_rate" : popularity_rate,
                "satisfaction_rate" : satisfaction_rate,
                "total_reviews" : total_reviews,
                "uidentifier" : uidentifier,
                "average_price" : average_price
            }


        # Get and store all the segments
        segments = {}

        list_of_segments = self.mySqlDB.raw_consultant_query(
            f"SELECT uidentifier, name, size FROM Segment;")

        for segment in list_of_segments:
            segmentUID, name, size = segment
            segments[segmentUID] = {"name" : name, "size" : size, "uidentifier" : segmentUID, "restaurants" : []}
        

        # Get the associations between both tables, and add each segment to the corresponding restaurants
        list_of_associations = self.mySqlDB.raw_consultant_query(
            f"SELECT restaurantUID, segmentUID FROM Restaurant_Segment_Association;")

        for association in list_of_associations:
            restaurantUID, segmentUID = association
            segments[segmentUID]["restaurants"].append(restaurants[restaurantUID])

        return str(json.dumps(segments, indent=4))
        # self.mySqlDB.consultant_query()