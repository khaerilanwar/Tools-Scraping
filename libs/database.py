import mysql.connector
from prettytable import from_db_cursor


class Database:
    def __init__(self, host: str, username: str, password: str, database: str):
        self.mydb = mysql.connector.connect(
            host=host, user=username, password=password, database=database
        )
        self.mycursor = self.mydb.cursor()
        self.separator = ", "

    def select(self, table: str, field: list = []) -> None:
        """
        param1: an str value (where table for view)
        param2: an list value (select field for view)
        """

        if len(field) != 0:
            # create name column
            self.fields = self.separator.join(field)
            self.query = f"SELECT {self.fields} FROM {table}"

        else:
            # create variabel for query
            self.query = f"SELECT * FROM {table}"

        # execute query
        self.mycursor.execute(self.query)

        self.result = from_db_cursor(self.mycursor)
        self.result.align = "l"
        return self.result

    def insert(self, name_table: str, data: dict):
        # name field table
        self.column = self.separator.join(list(data.keys()))
        # data for insert data
        # self.row = ", ".join(['"{}"'.format(word) for word in list(data.values())])
        self.row = ", ".join(['"{}"'.format(word) for word in list(data.values())])
        # query to insert data in database
        self.query = f"INSERT INTO {name_table} ({self.column}) VALUES ({', '.join(['%s' for i in range(len(data))])})"
        self.mycursor.execute(self.query, tuple(data.values()))
        self.mydb.commit()

        return self.mycursor.rowcount, "record inserted."


# examp = Database("localhost", "root", "", "db_tegal")

# data = {
#     'nama': 'Rumput Laut hijau',
#     'harga': '15000',
#     'user': 'anwar'
# }
# examp.insert('belajar', data)
