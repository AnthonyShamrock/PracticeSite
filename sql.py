# # # # # # # # # # # # #
#  TESTING SQL PROGRAM  #
# # # # # # # # # # # # #

import sqlite3
 
connection = sqlite3.connect("website.db")
cursor = connection.cursor()


# connection.execute('''
#    CREATE TABLE questions (
#        id INTEGER PRIMARY KEY,
#        question TEXT NOT NULL,
#        answer TEXT NOT NULL
#    );
#''')

connection.execute('''CREATE TABLE questions (
    id INTEGER PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);''')


#connection.execute("INSERT INTO questions (question, answer) VALUES ('Test', 'Testing')")
connection.commit()
print(cursor.execute("SELECT * FROM questions").fetchall())
