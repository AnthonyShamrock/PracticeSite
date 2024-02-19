import sqlite3 

class sql():
    def __init__(self):
        self.connection = sqlite3.connect("instance/website.db")
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        s = self.cursor.execute(query, params)
        self.connection.commit()
        return s
    
    def close(self):
        self.connection.close()