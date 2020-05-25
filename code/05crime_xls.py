import pandas as pd 
import sqlite3

conn = sqlite3.connect('C:/db/05_crime.db')
c = conn.cursor()
c.execute('''CREATE TABLE crime15
          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
          ADDRESS TEXT NOT NULL,
          TOTAL INTEGER NOT NULL,
          THUG INTEGER NOT NULL,
          VIOLENT INTEGER NOT NULL,
          INTHEFT INTEGER NOT NULL,
          THEFT INTEGER NOT NULL);''')
conn.commit()
conn.close()

path = 'C:/data/05_crime/H27.xls'
for i in range(63):
    df = pd.read_excel(path,sheet_name=i)
    for j in range(6,500):
        try:
            conn = sqlite3.connect('C:/db/05_crime.db')
            c = conn.cursor()
            c.execute(
                "INSERT INTO crime15 (ID,ADDRESS,TOTAL,THUG,VIOLENT,INTHEFT,THEFT) \
                    VALUES (NULL,?,?,?,?,?,?)",
                    (df.iloc[j,0],df.iloc[j,1],df.iloc[j,2],df.iloc[j,5],df.iloc[j,11],df.iloc[j,20]));
            conn.commit()
            conn.close()
        except Exception:
            pass