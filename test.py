import sqlite3

con = sqlite3.connect('users4.db')

cursor = con.cursor()


cursor.execute('select * from USERS')
for i in cursor:
    print(i)
con.commit()
con.close()