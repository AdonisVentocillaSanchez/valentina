import sqlite3

con = sqlite3.connect('Proyecto_Linio.db')
cursor = con.cursor()

cursor.execute('SELECT * FROM comercio')
rows = cursor.fetchall()
for row in rows:
    print(row)