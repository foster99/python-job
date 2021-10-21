from MongoDB_connector import MongoDB_connector
import json

class Restaurants_MongoDB_manager:

    def __init__(self, url, port, user, password, db_name):

        self.URL = url
        self.PORT = port
        self.USER = user
        self.PASSWORD = password
        self.DB_NAME = db_name
        self.dbm = MongoDB_connector(url=self.URL, 
                                    port=self.PORT, 
                                    user=self.USER, 
                                    password=self.PASSWORD)
    
    def query_restaurants(self, params:dict):

        # Add '$' before operator to adapt the filter to the MongoDB format
        correct_format = True
        formated_params = {}
        for field, operator_value in params.items():

            if type(operator_value) != dict or len(operator_value) != 1:
                correct_format = False
                break

            for operator,value in operator_value.items():
                formated_params[field] = {f"${operator}" : value}
        
        # Check if we have dectected a format error
        if not correct_format:
            print("The params were not correctly formated. Aborting query ...")
            return []

        # Check DB connection
        if not self.dbm.is_connected():
            self.dbm.connect_to_db(self.DB_NAME)

        # Query the restaurants
        return list(self.dbm.db_find_in_collection('Restaurant', formated_params))

    def import_restaurants_and_segments_from_file_to_dict(self, restaurant_data_path, segment_data_path):

        # Create a dictionaries for restaurants and segments, both indexed by their UID to avoid repetitions.
        restaurants = {}
        segments = {}

        # Load restaurants
        with open(restaurant_data_path) as json_restaurant_file:

            # Load list of objects from JSON file
            restaurant_list = json.load(json_restaurant_file)

            for restaurant in restaurant_list:

                # Add each restaurant of the list to the dictionary (avoiding repetitions)
                restaurants[restaurant['uidentifier']] = restaurant

                restaurant['average_price'] = float(restaurant['average_price'])

                # We also add a new field to store the segment UID to which it belong
                restaurant['segment_uids'] = []

        # Load segments
        with open(segment_data_path) as json_segment_file:
            
            # Load list of objects from JSON file
            segment_list = json.load(json_segment_file)

            for segment in segment_list:

                # Add each segment of the list to the dictionary (avoiding repetitions)
                segments[segment['uidentifier']] = {
                    "name": segment["name"],
                    "size": segment["size"],
                    "uidentifier": segment["uidentifier"],
                    "average_popularity_rate": segment["average_popularity_rate"],
                    "average_satisfaction_rate": segment["average_satisfaction_rate"],
                    "average_price": segment["average_price"],
                    "total_reviews": segment["total_reviews"]
                }

                # Add the reference of the current segment to each associated restaurant
                for restaurant_uid in segment['restaurants']:
                    restaurants[restaurant_uid]['segment_uids'].append(segment['uidentifier'])

        return (restaurants, segments)
        
    def import_restaurants_and_segments_from_dict_to_db(self, restaurants, segments):
        
        if not self.dbm.is_connected():
            self.dbm.connect_to_db(self.DB_NAME)
        
        # Insert Restaurants
        self.dbm.db_insert_many_documents_in_collection('Restaurant', restaurants.values())

        # Insert Segments
        self.dbm.db_insert_many_documents_in_collection('Segment', segments.values())

        # Compute Segment derivated fields

        pipeline = [
            {
                "$lookup" : {
                    "from" : "Restaurant",
                    "let" : {"segmentUID" : "$uidentifier"},
                    "pipeline": [ {
                        "$match": {
                            "$expr": { "$in": [ "$$segmentUID", "$segment_uids" ] } 
                        }
                    } ],
                    "as": "segment_restaurants"
                } 
            },
            
            {
                "$set": { 
                    "average_popularity_rate" : { "$avg": "$segment_restaurants.popularity_rate" },
                    "average_satisfaction_rate" : { "$avg": "$segment_restaurants.satisfaction_rate"},
                    "average_price" : {"$avg": "$segment_restaurants.average_price"},
                    "total_reviews" : {"$sum": "$segment_restaurants.total_reviews"}
                }
            },
            
            {
        	    "$project" : {
                    "_id" : 1,
                    "average_popularity_rate" : 1,
                    "average_satisfaction_rate" : 1,
                    "average_price" : 1,
                    "total_reviews" : 1
        	    }
            }
        ]
        
        aggregation_result = self.dbm.db_aggregate_in_collection('Segment', pipeline)

        for segment_data in aggregation_result:

            filter_ = {"_id" : segment_data["_id"]}
            update_ = {

                "$set" : {
                    "average_popularity_rate" : str(segment_data["average_popularity_rate"]),
                    "average_satisfaction_rate" : str(segment_data["average_satisfaction_rate"]),
                    "average_price" : str(segment_data["average_price"]),
                    "total_reviews" : str(segment_data["total_reviews"])
                }
            }

            self.dbm.db_update_one_in_collection('Segment', filter_, update_)

    def get_list_of_all_restaurants_without_segment_data(self):

        if not self.dbm.is_connected():
            self.dbm.connect_to_db(self.DB_NAME)

        filter = { }
        projection = {'_id' : 0, 'segment_uids' : 0 }

        return list(self.dbm.db_find_in_collection('Restaurant', filter, projection))

    def get_list_of_all_segments(self):

        if not self.dbm.is_connected():
            self.dbm.connect_to_db(self.DB_NAME)

        query = { }
        projection = {'_id' : 0}

        return list(self.dbm.db_find_in_collection('Segment', query, projection))

    def get_restaurants_uids_of_segment(self, segmentUID):

        if not self.dbm.is_connected():
            self.dbm.connect_to_db(self.DB_NAME)

        filter = { 'segment_uids' : { '$elemMatch' : { '$eq' : segmentUID } } }
        projection = { '_id' : 0, 'uidentifier' : 1 }

        return list(self.dbm.db_find_in_collection('Restaurant', filter, projection))

    def insert_many_restaurants(self, restaurant_list) -> bool:

        if not self.dbm.is_connected():
            self.dbm.connect_to_db(self.DB_NAME)
        
        return self.dbm.db_insert_many_documents_in_collection('Restaurant', restaurant_list)

    def insert_many_segments(self, segment_list) -> bool:

        if not self.dbm.is_connected():
            self.dbm.connect_to_db(self.DB_NAME)
        
        return self.dbm.db_insert_many_documents_in_collection('Segment', segment_list)

    def drop_all_collections(self):

        if not self.dbm.is_connected():
            self.dbm.connect_to_db(self.DB_NAME)
        
        drop1 = self.dbm.db_drop_collection('Restaurant')
        drop2 = self.dbm.db_drop_collection('Segment')
        
        return drop1 and drop2

    def export_all_data_to_file(self, path):

        pipeline = [
            {
                "$lookup": {
                    "from": "Restaurant",
                    "let": { "segmentUID": "$uidentifier"},
                    "pipeline": [ {
                        "$match": {
                            "$expr": { "$in": [ "$$segmentUID", "$segment_uids" ] } 
                        }
                    } ],
                    "as" : "segment_restaurants"
                }
            },
            # {
            #     "$unwind" : "$segment_restaurants"
            # },
            {
                "$project" : {
                    "_id" : 0,
                    "average_popularity_rate" : 0,
                    "average_satisfaction_rate" : 0,
                    "average_price" : 0,
                    "total_reviews" : 0,
                    "segment_restaurants._id" : 0,
                    "segment_restaurants.segment_uids" : 0,
                }
            },
            {
                "$project" : {
                    "name" : 1,
                    "size" : 1,
                    "uidentifier" : 1,
                    "restaurants" : "$segment_restaurants"
                }
            }
        ]

        # Check DB connection
        if not self.dbm.is_connected():
            self.dbm.connect_to_db(self.DB_NAME)

        segment_list = self.dbm.db_aggregate_in_collection('Segment', pipeline)
        

        json_data = {}
        for segment in segment_list:
            json_data[segment['uidentifier']] = segment
        
        file = open(path,"w")
        file.write(str(json.dumps(json_data, indent=4)))
        file.close()
        