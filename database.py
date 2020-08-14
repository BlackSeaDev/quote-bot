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
            # Language table
            """
            CREATE TABLE IF NOT EXISTS "Language" (
                "chat_id" INTEGER NOT NULL,
                "lang"    INTEGER
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
        sql2 = 'CREATE UNIQUE INDEX idx_Language_chat_id ON Language (chat_id)'
        self.execute_sql([sql2])


    def setLang(self, chat_id: int, lang: int) -> None:
        sql = 'INSERT OR REPLACE INTO Language (chat_id, lang) VALUES (?, ?)'
        args = [chat_id, lang]
        self.execute_sql([sql, args])

    def getLang(self, chat_id: int) -> int:
        sql = 'SELECT EXISTS(SELECT * from Language Where chat_id = ?)'
        args = [chat_id]
        # print(chat_id)
        self.execute_sql([sql, args])
        if self.cursor.fetchall()[0][0] == 0:
            return None
        else:
            sql = 'SELECT lang from Language Where chat_id = ?'
            args = [chat_id]
            self.execute_sql([sql, args])
            return self.cursor.fetchall()[0][0]

    def randomFact(self) -> str:
        sql = 'SELECT * FROM Facts ORDER BY random() LIMIT 1'
        self.execute_sql([sql])
        fact = self.cursor.fetchall()[0][0]
        return fact

    def updateFacts(self, facts: list) -> int:
        sql = 'DELETE FROM Facts'
        self.execute_sql([sql])

        sql = 'INSERT INTO Facts (Fact) VALUES (?)'
        args = facts
        self.execute_sql([sql,args],many=True)
        return len(facts)


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
    print(DB.randomFact())

    # print(db.get_users("new"))
    # print(checkUser(100))
    # clearUsers()
    pass
