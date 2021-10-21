import urllib.parse
import DB_migrator

def main():

    # Databases connection info

    mySQL_credentials = {
        "DB_URL"  : 'sfexam.delectame.develop',
        "DB_NAME" : 'exam_dev',
        "DB_USER" : 'root',
        "DB_PASS" : 'delectaRoot1234!'
    }

    mongoDB_credentials = {
        "DB_URL"  : "192.168.70.70",
        "DB_PORT" : '27017',
        "DB_NAME" : "delectaDatabase",
        "DB_USER" : urllib.parse.quote_plus("delecta_root"),
        "DB_PASS" : urllib.parse.quote_plus("delectaRoot1234!")
    }

    
    # Migrate from Mongo to MySQL

    print("Clearing MySQL data ...")
    if DB_migrator.clear_mySQL(mySQL_credentials):
        print("Cleared succesfully.")
    else:
        print("Error clearing the data.")
        print("Exiting migrator...")
        exit(1)

    print("Migrating MySQL data to MongoDB ...")
    if DB_migrator.migrate_from_mongoDB_to_mySQL(MongoDB_credentials=mongoDB_credentials,
                                                MySQL_credentials=mySQL_credentials):
        print("Migrated succesfully.")
    else:
        print("Error migrating the data.")
        print("Exiting migrator...")
        exit(1)


if __name__ == "__main__":
    main()
