import csv
import sqlite3

conn = sqlite3.connect('C:/data/02_earthquake.db')
c = conn.cursor()
c.execute('''CREATE TABLE earth17
          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
          LAT REAL NOT NULL,
          LON REAL NOT NULL,
          Y30W5 REAL NOT NULL,
          Y30S5 REAL NOT NULL,
          Y30W6 REAL NOT NULL,
          Y30S6 REAL NOT NULL);''')
conn.commit()
conn.close()

path = 'C:/data/02_earthquake/P-Y2017-MAP-AVR-TTL_MTTL-5339/P-Y2017-MAP-AVR-TTL_MTTL-5339/P-Y2017-MAP-AVR-TTL_MTTL-5339.csv'
with open(path, newline='') as csvfile:
    rows = csv.reader(csvfile, skipinitialspace=True, delimiter=',')
    next(rows)
    for row in rows:
        
        mesh10 = str(row[0])
        p = int(mesh10[0:2])
        u = int(mesh10[2:4])
        q = int(mesh10[4:5])
        v = int(mesh10[5:6])
        r = int(mesh10[6:7])
        w = int(mesh10[7:8])
        m = int(mesh10[8:9])
        n = int(mesh10[9:])
        
        if m == 1:
            s = 0
            x = 0
        elif m == 2:
            s = 0
            x = 1
        elif m ==3:
            s = 1
            x = 0
        else:
            s = 1
            x = 1
        
        if n == 1:
            t = 0
            y = 0
        elif n == 2:
            t = 0
            y = 1
        elif n ==3:
            t = 1
            y = 0
        else:
            t = 1
            y = 1
        
        lat = round(t * 7.5 / 3600 + s * 15 / 3600 + r / 120 + q / 12 + p * 2 / 3, 5)
        lon = round(y * 11.25 / 3600 + x * 22.5 / 3600 + w / 80 + v / 8 + u + 100, 5)
        
        if lat < 35.89833:
            if lat > 35.50139:
                if lon < 139.91861:
                    if lon > 138.94306:
                        conn = sqlite3.connect('C:/db/02_earthquake.db')
                        c = conn.cursor()
                        c.execute(
                            "INSERT INTO earth17 (ID,LAT,LON,Y30W5,Y30S5,Y30W6,Y30S6) \
                                VALUES (NULL,?,?,?,?,?,?)",
                                (lat,lon,row[1],row[2],row[3],row[4]));
                        conn.commit()
                        conn.close()