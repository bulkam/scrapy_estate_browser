import sqlite3 as lite

class DB:

    def __init__(self, name:str):
        self.con = lite.connect(name)
    
    def create_table(self):
        with self.con:
            self.cur = self.con.cursor()
            try:
                self.cur.execute("CREATE TABLE estates(id INT, name TEXT, url TEXT)")
            except:
                return

    def insert_row(self, row:list):
        if not len(row) == 3:
            return
        with self.con:
            self.cur.execute("INSERT INTO  estates VALUES(%s, '%s', '%s')" % row)
    
if __name__ == "__main__":
    db = DB("estates.db")
    db.create_table()
    for row in db.cur.execute("SELECT * FROM estates"):
        print(row)