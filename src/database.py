import sqlite3
import datetime
from os import getcwd, path
from datetime import datetime
from inspect import currentframe



class DbInterface:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        sql_tables = [
            # Users table
            """
            CREATE TABLE IF NOT EXISTS "Users" (
                "chat_id" INTEGER NOT NULL,
                "lang"    INTEGER,

                PRIMARY KEY (chat_id)
            )
            """,
            # Quotes table
            """
            CREATE TABLE IF NOT EXISTS "Quotes" (
                "user_id" INTEGER NOT NULL,
                "q_id"    INTEGER PRIMARY KEY AUTOINCREMENT,
                "quote"   TEXT NOT NULL,
                "q_owner" TEXT,

                FOREIGN KEY (user_id) REFERENCES Users(chat_id)
            )
            """,
        ]

        for sql in sql_tables:
            self.cursor.execute(sql)
            self.conn.commit()

    
    # safely executes sql request
    def execute_sql(self, sql_and_args: list, many = False) -> None:
        try:
            if many:
                self.cursor.executemany(*sql_and_args)
            else:
                self.cursor.execute(*sql_and_args)
        except Exception as e:
            function_name = currentframe().f_back.f_code.co_name
            print(f"[ERROR] {function_name}\n{e}\n")
        finally:
            self.conn.commit()
    
    def idx(self) -> None: # creates unique indexes to make impossible to write the same chat_id in BD twi
        sql2 = 'CREATE UNIQUE INDEX idx_Users_chat_id ON Users (chat_id)'
        self.execute_sql([sql2])


    def setLang(self, chat_id: int, lang: int) -> None:
        sql = 'INSERT OR REPLACE INTO Users (chat_id, lang) VALUES (?, ?)'
        args = [chat_id, lang]
        self.execute_sql([sql, args])

    def getLang(self, chat_id: int) -> int:
        sql = 'SELECT EXISTS(SELECT * from Users Where chat_id = ?)'
        args = [chat_id]
        # print(chat_id)
        self.execute_sql([sql, args])
        if self.cursor.fetchall()[0][0] == 0:
            return None
        else:
            sql = 'SELECT lang from Users Where chat_id = ?'
            args = [chat_id]
            self.execute_sql([sql, args])
            return self.cursor.fetchall()[0][0]

    def getRandomQuote(self, user_id: int) -> str:
        sql = 'SELECT * FROM Quotes Where user_id = ? ORDER BY random() LIMIT 1'
        args = [user_id]
        self.execute_sql([sql, args])
        result = self.cursor.fetchall()

        try:
            quote, q_owner = result[0][2], result[0][3]
            # print(quote, q_owner)

        except Exception as e:
            print(f'Exception appeared: {e}')
            quote, q_owner = None, None

        return quote, q_owner

    def getFullListOfQuotes(self, user_id: int) -> list:
        sql = 'SELECT * FROM Quotes Where user_id = ?'
        args = [user_id]
        self.execute_sql([sql, args])
        result = [i[2:] for i in self.cursor.fetchall()]
        # print(result)
        return result

    def addNewQuote(self, user_id: int, quote: str, q_owner: str) -> None:
        if q_owner == 'None':
            sql = 'INSERT INTO Quotes (user_id, quote) VALUES (?, ?)'
            args = [user_id, quote]
            self.execute_sql([sql, args])
        else:
            sql = 'INSERT INTO Quotes (user_id, quote, q_owner) VALUES (?, ?, ?)'
            args = [user_id, quote, q_owner]
            self.execute_sql([sql, args])


# setting up the database
def start_database():
    print()
    database = "Quote_bot_DB.db"
    # if no db file -> create one
    if not path.exists(database):
        print("no database found")
        create_path = path.abspath(getcwd())
        create_path = path.join(create_path, database)
        print(f"create_path: {create_path}")
        f = open(create_path, "x")
        f.close()
    else:
        print("Database exist")
    full_path = path.abspath(path.expanduser(path.expandvars(database)))
    print(f"full_path: {full_path}")
    DB = DbInterface(full_path)
    return DB
DB = start_database()


if __name__=="__main__":
    # print(updateFact())
    # print(DB.getRandomQuote())

    # print(db.get_users("new"))
    # print(checkUser(100))
    # clearUsers()
    pass
