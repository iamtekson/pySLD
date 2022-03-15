from psycopg2 import sql, connect


class Pg:
    def __init__(self, dbname=None, user='postgres', password='admin', host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.schema = None
        self.conn = None

    def connect(self):
        try:
            self.conn = connect(
                dbname=self.dbname,
                user=self.user,
                host=self.host,
                password=self.password
            )

        except Exception as err:
            print("psycopg2 connect() ERROR:", err)
            self.conn = None

    # Execute sql query
    def execute_sql(self, cursor, sql):
        try:
            cursor.execute(sql)

        except Exception as err:
            return ('ERROR: ', err)

    def set_postgres_schema(self, schema):
        self.schema = schema

    # get the columns names inside database
    def get_column_names(self, table):
        columns = []
        with self.conn.cursor() as col_cursor:
            col_names_str = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE "
            col_names_str += "table_name = '{}';".format(table)
            sql_object = sql.SQL(col_names_str).format(
                sql.Identifier(table))
            try:
                col_cursor.execute(sql_object)
                col_names = (col_cursor.fetchall())
                for tup in col_names:
                    columns += [tup[0]]

            except Exception as err:
                return ("get_columns_names ERROR:", err)

        return columns

    # get all the values from specific column
    def get_values_from_column(self, column, table, schema="public", distinct=True):
        values = []
        with self.conn.cursor() as col_cursor:
            if distinct:
                all_values_str = '''SELECT DISTINCT "{0}" FROM "{2}"."{1}" ORDER BY "{0}";'''.format(
                    column, table, schema)
            else:
                all_values_str = '''SELECT "{0}" FROM "{2}"."{1}" ORDER BY "{0}";'''.format(
                    column, table, schema)

            sql_object = sql.SQL(all_values_str).format(
                sql.Identifier(column), sql.Identifier(table))

            try:
                col_cursor.execute(sql_object, (column))
                values_name = (col_cursor.fetchall())
                for tup in values_name:
                    values += [tup[0]]

            except Exception as err:
                return ("get_columns_names ERROR:", err)

        return values

    # get all the values from specific column
    def get_values_from_sql(self, sql_query):
        values = []
        with self.conn.cursor() as col_cursor:
            try:
                col_cursor.execute(sql_query)
                values_name = (col_cursor.fetchall())
                for tup in values_name:
                    values += [tup[0]]

            except Exception as err:
                return ("get_columns_names ERROR:", err)

        return values

    # create the schema based on the given name
    def create_schema(self, name):
        n = name.split(' ')
        if len(n) > 0:
            name = name.replace(' ', '_')

        with self.conn.cursor() as cursor:
            sql = f'''CREATE SCHEMA IF NOT EXISTS {name}'''
            self.execute_sql(cursor, sql)
            self.conn.commit()
            return ('Schema create successfully')

    # create new column in table
    def create_column(self, column, table,  col_datatype='varchar', schema='public',):

        with self.conn.cursor() as cursor:
            sql = '''ALTER TABLE "{3}"."{0}" ADD IF NOT EXISTS "{1}" {2}'''.format(
                table, column, col_datatype, schema)
            self.execute_sql(cursor, sql)
            self.conn.commit()
            return ('create column successful')

    # update column
    def update_column(self, column, value, table, schema, where_column, where_value):
        with self.conn.cursor() as cursor:
            sql = '''
                UPDATE "{0}"."{1}" SET "{2}"='{3}' WHERE "{4}"='{5}'
                '''.format(
                schema, table, column, value, where_column, where_value)
            self.execute_sql(cursor, sql)
            self.conn.commit()
            return ('update table successful')

    # delete table
    def delete_table(self, name, schema):
        with self.conn.cursor() as cursor:
            sql = '''DROP TABLE IF EXISTS "{}"."{}" CASCADE;'''.format(
                schema, name)
            self.execute_sql(cursor, sql)
            self.conn.commit()
            return ('{} table dropped successfully.'.format(name))

    # Delete values
    def delete_values(self, table_name, schema, condition):
        with self.conn.cursor() as cursor:
            sql = '''DELETE FROM "{}"."{}" WHERE {}'''.format(
                schema, table_name, condition)
            self.execute_sql(cursor, sql)
            self.conn.commit()
            return ('Values dropped successfully.')
