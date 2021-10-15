import mysql.connector
from mysql.connector import Error, connect, errorcode
from mysql.connector import connection

class MySQL_connector:

    def __init__(self):
        self.connection  = None

    def connect_to_database(self, DB_url_, DB_name_, DB_user_, DB_pass_) -> bool:

        try:
            self.connection = mysql.connector.connect(host=DB_url_,
                                                database=DB_name_,
                                                user=DB_user_,
                                                password=DB_pass_)
            if self.connection.is_connected():
                
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

                return True

        except Error as e:
            print("Error while connecting to MySQL", e)
            return False

    def create_database(self, DB_name_) -> bool:

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        
        else:
            print("There is not a connection to the database")

        try:
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_name_))
            print("Database {} created successfully.".format(DB_name_))

        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def select_database(self, DB_name_, create_if_missing=True) -> bool:

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return False

        try:
            cursor.execute("USE {}".format(DB_name_))
            cursor.close()
            print(f"Database {DB_name_} has been selected succesfully.")
            return True
            
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_name_))
            if create_if_missing and err.errno == errorcode.ER_BAD_DB_ERROR:
                return self.create_database(DB_name_)
            else:
                print(err)
                return False

    def add_tables_to_database(self, tables) -> bool:

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return False

        for table_name in tables:

            table_description = tables[table_name]
            
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(f"The table {table_name} already exists.")
                else:
                    print(err.msg)
                    return False
            else:
                print(f"Table {table_name} has been succesfully created.")
        
        return True

    def close_database_connection(self) -> bool:

        if self.connection.is_connected():
            self.connection.close()
            print("Database connection has been succesfully closed.")
            return True
        else:
            print("There is not a connection to the database")
            return False

    def drop_table(self, table_name) -> bool:

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return False

        delete_table_sentence = f"DROP TABLE IF EXISTS {table_name}"

        try:
            print("Dropping table {}: ".format(table_name), end='')
            cursor.execute(delete_table_sentence)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(f"The table {table_name} already exists.")
            else:
                print(err.msg)
                return False
        else:
            print(f"Table {table_name} has been succesfully droped.")
        
        return True
    
    def show_tables(self):
        
        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return False

        try:
            print("Showing all the tables:")
            cursor.execute("SHOW Tables")
            print(cursor.fetchall())
            return True

        except mysql.connector.Error as err:
            print(err.msg)
            return False
    
    def describe_table(self, table_name):

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return False

        try:
            print(f"Describing table {table_name}:")
            cursor.execute(f"DESCRIBE {table_name}")
            
            for x in cursor.fetchall():
                print(f"  -> {x}")

            return True

        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def show_columns_from_table(self, table_name):

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return False

        try:
            print(f"Showing columns from table {table_name}:")
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")

            for x in cursor.fetchall():
                print(f"  -> {x}")
            
            return True

        except mysql.connector.Error as err:
            print(err.msg)
            return False
        
    def insertInTable(self, table_name, column_names, values):

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return False
        
        
        print(f"Inserting values into table {table_name}:")

        # format column_names to MySQL format
        formated_column_names = ""
        for column in column_names:
            formated_column_names += column + ","
        formated_column_names = formated_column_names[:-1]


        formated_values = ""
        skipCommaRow = True
        for row in values:
            
            if not skipCommaRow:
                formated_values += ","
            else:
                skipCommaRow = False

            formated_values += "\n("

            skipCommaField = True
            # format rows to MySQL format
            for field in row:
                if not skipCommaField:
                    formated_values += ","
                else:
                    skipCommaField = False
                formated_values += str(field)
            
            formated_values += ")"
            
        try:
            # print(f"INSERT INTO {table_name} ({formated_column_names}) VALUES {formated_values};")
            cursor.execute(f"INSERT INTO {table_name} ({formated_column_names}) VALUES {formated_values};")
            self.connection.commit()
        except mysql.connector.Error as err:
            # if err.errno != errorcode.ER_DUP_ENTRY:
            print(err.msg)

        """
            for row in values:
            
            formated_values = ""
            skipComma = True
            # format rows to MySQL format
            for field in row:
                if not skipComma:
                    formated_values += ","
                else:
                    skipComma = False
                formated_values += str(field)
            
            try:
                # print(f"INSERT INTO {table_name} ({formated_column_names}) VALUES {formated_values};")
                cursor.execute(f"INSERT INTO {table_name} ({formated_column_names}) VALUES ({formated_values});")
                self.connection.commit()
            except mysql.connector.Error as err:
                # if err.errno != errorcode.ER_DUP_ENTRY:
                print(err.msg)
        """
                
        return True    

    def set_derived_value(self, table_name, attribute, scalar_subquery, table_alias=""):

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return False

        try:
            print(f"Setting attribute {attribute} from table {table_name}:")

            cursor.execute(f"UPDATE {table_name} {table_alias} SET {attribute} = ({scalar_subquery});")
            self.connection.commit()
            return True

        except mysql.connector.Error as err:
            print(err.msg)
            return False
    
    def consultant_query(self, query) -> str:

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return "Query Error"

        try:
            print(f"Launching query {query}:")
            cursor.execute(query)

            returned_value = ""
            count = 0
            for x in cursor.fetchall():
                returned_value += f"  -> {x}\n"
                count += 1

            if cursor.rowcount == 0:
                returned_value = "-> There is not a restaurant that satifies the given conditions.\n" + returned_value
            else:
                returned_value = f"-> The database returned {cursor.rowcount} restaurants:\n" + returned_value

            return returned_value

        except mysql.connector.Error as err:
            print(err.msg)
            return "Query Error"
    
    def raw_consultant_query(self, query) -> str:

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return "Query Error"

        try:
            print(f"Launching query {query}:")
            cursor.execute(query)

            returned_value = []
            for x in cursor.fetchall():
                returned_value.append(x)
                
            return returned_value

        except mysql.connector.Error as err:
            print(err.msg)
            return "Query Error"

    