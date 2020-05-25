from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('C:/db/03_train.db')
c = conn.cursor()
c.execute('''CREATE TABLE train18
          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
          EKITYPE INTEGER NOT NULL,
          EKISPTYPE INTEGER NOT NULL,
          EKILINE TEXT NOT NULL,
          EKICOMPANY TEXT NOT NULL,
          EKINAME TEXT NOT NULL);''')
conn.commit()
conn.close()

path = 'C:/data/03_train/N02-18_GML/N02-18.xml'
file = open(path,'r',encoding='utf-8_sig')
soup = BeautifulSoup(file, 'lxml-xml')

company = ['ゆりかもめ','京王電鉄','京成電鉄','京浜急行電鉄','埼玉高速鉄道','首都圏新都市鉄道','小田急電鉄','西武鉄道',
           '多摩都市モノレール','東京モノレール','東京急行電鉄','東京地下鉄','東京都','東京臨海高速鉄道','東日本旅客鉄道','東武鉄道']

result_eki = soup.find_all('ksj:Station')
for i in result_eki:
    railwayType = i.find('ksj:railwayType').text
    serviceProviderType = i.find('ksj:serviceProviderType').text
    railwayLineName = i.find('ksj:railwayLineName').text
    operationCompany = i.find('ksj:operationCompany').text
    stationName = i.find('ksj:stationName').text
    
    if operationCompany in company:
        conn = sqlite3.connect('C:/db/03_train.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO train18 (ID,EKITYPE,EKISPTYPE,EKILINE,EKICOMPANY,EKINAME) \
                VALUES (NULL,?,?,?,?,?)",
                (railwayType,serviceProviderType,railwayLineName,operationCompany,stationName));
        conn.commit()
        conn.close()