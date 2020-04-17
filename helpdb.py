"""
Module to read and write username and points to scoring database
"""
import sqlite3


class CreateDB:
    """
    Class to create and make connection to DB
    """

    def __init__(self):
        """
        Initiating connection
        """
        self.conn = sqlite3.connect("HS.db")
        self.curs = self.conn.cursor()

    def create(self):
        """
        Creating database tables for scoring
        """
        try:
            self.curs.execute("""
            CREATE TABLE HighScore  (
            db_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            score INTEGER);""")
            print('Creating DataBase is successful!')
            return self.conn
        except sqlite3.Error as error:
            print(error)
            return self.conn


class ReadDB(CreateDB):
    """
    Class to read score to database
    """

    def read_db(self):
        """ Reading Username and Score from DB """

        with self.conn:
            self.curs.execute("""
            SELECT ROW_NUMBER() OVER(ORDER BY score DESC) AS Place, name, score, db_id
            FROM HighScore;""")
        return self.curs.fetchall()

    def read_high_db(self):
        """ Reading highest score from DB """

        with self.conn:
            self.curs.execute("""SELECT MAX(score) FROM HighScore;""")
        return self.curs.fetchall()


class WriteDB(CreateDB):
    """
    Class to write score from database
    """

    def __init__(self, name, score):
        """Initiating data for writing to DB"""
        super().__init__()
        self.username = name
        self.score = score
        self.db_id = None

    def write_to_db(self):
        """ Writing Username and Score to DB """

        # Checking the existence of data for recording to DB
        #
        # print(self.username)
        #
        # if self.username is None or self.score < 2:
        #     print("There are no db to write!")
        # else:
        #     with self.conn:
        #         self.curs.execute("INSERT INTO HSDB VALUES (?,?,?)",
        #                           (self.db_id, self.username, self.score))
        #
        #         print("Score was added successful!")

        with self.conn:
            self.curs.execute("INSERT INTO HighScore VALUES (?,?,?)",
                              (self.db_id, self.username, self.score))

            print("Score was added successful!")
