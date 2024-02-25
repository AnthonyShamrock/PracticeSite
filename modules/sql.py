import sqlite3 

class sql():
    def __init__(self):
        self.connection = sqlite3.connect("instance/website.db")
        self.cursor = self.connection.cursor()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
        
    def execute(self, query, params=None):
        returnStatement = None
        try: 
            if params:
                returnStatement = self.cursor.execute(query, params)
            else:
                returnStatement = self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise sqlite3.Error
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise Exception
        return returnStatement
        
    
    def close(self):
        self.connection.close()