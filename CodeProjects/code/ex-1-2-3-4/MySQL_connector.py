import mysql.connector
from mysql.connector import Error, connect, errorcode
from mysql.connector import connection

# Clase encargada de conectarse e interactuar con una base de datos MySQL.
class MySQL_connector:

    def __init__(self):
        self.connection  = None

    # Crea una conexion una base de datos mySQL dados su URL, nombre, usuario y contraseña
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

    # Crea una base de datos con el nombre pasado por parámetro en la conexión actual.
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

    # Selecciona una base de datos con el nombre pasado por parámetro en la conexión actual.
    # Admite un flag que crea dicha base de datos si esta no existe.
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

    # Añade un conjunto de tablas a la base de datos seleccionada en la conexión actual.
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

    # Cierra la conexión actual con la base de datos.
    def close_database_connection(self) -> bool:

        if self.connection.is_connected():
            self.connection.close()
            print("Database connection has been succesfully closed.")
            return True
        else:
            print("There is not a connection to the database")
            return False

    # Ejecuta el comando DROP sobre la tabla con el nombre dado en la base de datos seleccionada en la conexión actual.
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
    
    # Imprime en terminal las tablas que contiene la base de datos seleccionada en la conexión actual.
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
    
    # Ejecuta el comando DESCRIBE sobre la tabla con el nombre dado en la base de datos seleccionada en la conexión actual.
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

    # Ejecuta el comando SHOW COLUMNS FROM sobre la tabla con el nombre dado en la base de datos seleccionada en la conexión actual.
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
    
    def format_to_SQL(self, value):

        # null
        if value is None:
            return "NULL"
        
        # string
        if type(value) is str:
            return "\'" + str(value.replace('\'', '\\\'').replace('\\\\', '\\')) + "\'"

        # boolean
        if type(value) is bool:
            return str(value)
        
        # numeric
        return_value = float(value)

        if str(return_value).find('.') == -1:
            return str(int(value))      # int             
        return str(return_value)        # float

    # Inserta en la tabla referida por su nombre, en las columnas dadas, el conjunto de valores dado.
    def insertInTable(self, table_name, column_names, values, format_values=False) -> bool:

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return False
        
        
        print(f"Inserting values into table {table_name}:")

        if format_values:
            for row in values:
                for field in row:
                    format_values

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
                formated_values += str( self.format_to_SQL(field) if format_values else field )
            
            formated_values += ")"
            
        try:
            # print(f"INSERT INTO {table_name} ({formated_column_names}) VALUES {formated_values};")
            cursor.execute(f"INSERT INTO {table_name} ({formated_column_names}) VALUES {formated_values};")
            self.connection.commit()
            return True

        except mysql.connector.Error as err:
            # if err.errno != errorcode.ER_DUP_ENTRY:
            print(err.msg)
             
        return False    

    # Ejecuta el comando UPDATE/SET sobre la tabla referida por su nombre, asignando el valor resultante de la ScalarQuery pasada por parámetro, al atributo referido por su nombre.
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
    
    def _decode_value(self, init_value):

        value = init_value

        if (type(init_value) is bytearray):
            value = str(value, 'utf8')

        # null
        if value is None:
            return None

        # numeric
        try:
            return_value = float(value)

            if '.' in str(return_value):    # float
                return return_value
            else:                           # int
                return int(return_value)
        except:
            pass

        # boolean
        if str(value) == "True": return True
        if str(value) == "False": return False

        # string
        return str(value)

    # Ejecuta una consulta pasada por parámetro en la base de datos seleccionada en la conexión actual.
    def consultant_query(self, query, dict_=False, decode=True):

        if self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=dict_)
        else:
            print("There is not a connection to the database")
            return None

        try:
            print(f"Launching query {query}:")
            cursor.execute(query)

            if dict_:

                list_of_dicts = list(cursor.fetchall())

                if decode:
                    for dict_ in list_of_dicts:
                        for key in dict_.keys():
                            dict_[key] = self._decode_value(dict_[key])

                return list_of_dicts

            returned_value = ""
            count = 0
            for row in cursor.fetchall():
                if decode:
                    decoded_row = tuple([self._decode_value(value) for value in list(row)])
                    returned_value += f"  -> {decoded_row}\n"
                else:
                    returned_value += f"  -> {row}\n"
                count += 1

            return returned_value

        except mysql.connector.Error as err:
            print(err.msg)
            return None
    
    # Ejecuta una consulta pasada por parámetro en la base de datos seleccionada en la conexión actual y retorna las tuplas resultantes en formato de diccionario
    def consultant_query_to_json(self, query, decode=True):

        if self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
        else:
            print("There is not a connection to the database")
            return "Query Error"

        try:
            print(f"Launching query {query}:")
            cursor.execute(query)

            return cursor.fetchall()

        except mysql.connector.Error as err:
            print(err.msg)
            return "Query Error"

    # Ejecuta una consulta pasada por parámetro en la base de datos seleccionada en la conexión actual y las tuplas resultantes en una lista.
    def raw_consultant_query(self, query, decode=True):

        if self.connection.is_connected():
            cursor = self.connection.cursor()
        else:
            print("There is not a connection to the database")
            return "Query Error"

        try:
            print(f"Launching query {query}:")
            cursor.execute(query)

            returned_value = []
            for row in cursor.fetchall():
                if decode:
                    returned_value.append(tuple([self._decode_value(value) for value in list(row)]))
                else:
                    returned_value.append(row)
                
            return returned_value

        except mysql.connector.Error as err:
            print(err.msg)
            return "Query Error"

    