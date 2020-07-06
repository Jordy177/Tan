import pyodbc
import datetime


class Db:
    DRIVER = r'DRIVER={ODBC Driver 17 for SQL Server};'
    SERVER = r'SERVER=localhost;'
    DATABASE = r'DATABASE=master;'
    USERNAME = r'UID=sa;'
    PASSWORD = r'PWD=yourStrong(!)Password'

    def __init__(self):
        try:
            self._cnxn = pyodbc.connect(self.DRIVER + self.SERVER +
                                        self.DATABASE + self.USERNAME + self.PASSWORD, autocommit=True)
        except Exception:
            print('Connection cannot be made')

        self._cursor = self._cnxn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._cursor.close()
        self._cnxn.close()

    def get_version(self):
        self._cursor.execute("SELECT @@version;")
        row = self._cursor.fetchone()
        while row:
            print(row[0])
            row = self._cursor.fetchone()

    def _create_database(self):
        db_name = 'Temp' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self._cursor.execute('CREATE DATABASE {db}'.format(db = db_name))
        
        return db_name


    def create_table(self, script):
        db = self._create_database()     
        print(db)
        self._cursor.execute('USE {db}'.format(db = db))
        self._cursor.execute(script)