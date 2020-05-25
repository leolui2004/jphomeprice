import csv
import sqlite3

conn = sqlite3.connect('C:/db/05_crime.db')
c = conn.cursor()
c.execute('''CREATE TABLE crime19
          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
          ADDRESS TEXT NOT NULL,
          TOTAL INTEGER NOT NULL,
          THUG INTEGER NOT NULL,
          VIOLENT INTEGER NOT NULL,
          INTHEFT INTEGER NOT NULL,
          THEFT INTEGER NOT NULL);''')
conn.commit()
conn.close()

path = 'C:/data/05_crime/H31.csv'
with open(path, newline='') as csvfile:
    rows = csv.reader(csvfile, skipinitialspace=True, delimiter=',')
    next(rows)
    for row in rows:
        conn = sqlite3.connect('C:/db/05_crime.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO crime19 (ID,ADDRESS,TOTAL,THUG,VIOLENT,INTHEFT,THEFT) \
                VALUES (NULL,?,?,?,?,?,?)",
                (row[0],row[1],row[2],row[5],row[11],row[20]));
        conn.commit()
        conn.close()