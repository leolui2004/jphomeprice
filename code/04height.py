from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('C:/db/04_height.db')
c = conn.cursor()
c.execute('''CREATE TABLE height11
          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
          LAT REAL NOT NULL,
          LON REAL NOT NULL,
          HEIGHTAVG INTEGER NOT NULL,
          HEIGHTMAX INTEGER NOT NULL,
          HEIGHTMIN INTEGER NOT NULL);''')
conn.commit()
conn.close()

path = 'C:/data/04_height/G04-d-11_5339-jgd_GML/G04-d-11_5339-jgd.xml'
file = open(path,'r',encoding='utf-8_sig')
soup = BeautifulSoup(file, 'lxml-xml')

result_height = soup.find_all('gml:DataBlock')
for i in result_height:
    result_set = i.find('gml:tupleList').text
    result_split = result_set.split(',')
    
    for j in range(0,136,9):
        result_0 = result_split[j]
        mesh10 = result_0[-10:]
        result_1 = result_split[j+1]
        if result_1 != 'unknown':
            havg = int(float(result_1))
        result_2 = result_split[j+2]
        if result_2 != 'unknown':
            hmax = int(float(result_2))
        result_3 = result_split[j+3]
        if result_3 != 'unknown':
            hmin = int(float(result_3))

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
                        conn = sqlite3.connect('C:/db/04_height.db')
                        c = conn.cursor()
                        c.execute(
                            "INSERT INTO height11 (ID,LAT,LON,HEIGHTAVG,HEIGHTMAX,HEIGHTMIN) \
                                VALUES (NULL,?,?,?,?,?)",
                                (lat,lon,havg,hmax,hmin));
                        conn.commit()
                        conn.close()