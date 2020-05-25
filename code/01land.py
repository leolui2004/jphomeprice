from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('C:/db/01_land.db')
c = conn.cursor()

c.execute('''CREATE TABLE land19
          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
          LAT REAL NOT NULL,
          LON REAL NOT NULL,
          POS TEXT NOT NULL,
          PRICE INTEGER NOT NULL,
          CITY TEXT NOT NULL,
          ADDR TEXT NOT NULL,
          BLDUSE TEXT NOT NULL,
          STRU TEXT NOT NULL,
          WATER TEXT NOT NULL,
          GAS TEXT NOT NULL,
          SEWAGE TEXT NOT NULL,
          FLUP INTEGER NOT NULL,
          FLDOWN INTEGER NOT NULL,
          ROAD TEXT NOT NULL,
          ROADW REAL NOT NULL,
          NEAR TEXT NOT NULL,
          EKI TEXT NOT NULL,
          EKIDIST INTEGER NOT NULL,
          DISTUSE TEXT NOT NULL,
          FIRE TEXT NOT NULL,
          PLAN TEXT NOT NULL);''')
conn.commit()
conn.close()

path = 'C:/data/01_land/L01-19_13_GML/L01-19_13.xml'
file = open(path,'r',encoding='utf-8_sig')
soup = BeautifulSoup(file, 'lxml-xml')

result_gml = soup.find_all('gml:Point')
latitude = []
longitude = []
pos = []
for i in result_gml:   
    result_pos = i.find_all('gml:pos')
    for j in result_pos:
        pos_split = j.text.split(' ')
        lat = round(float(pos_split[0]),5)
        lon = round(float(pos_split[1]),5)
        latitude.append(lat)
        longitude.append(lon)
        position = '{},{}'.format(str(lat),str(lon))
        pos.append(position)

result_land = soup.find_all('ksj:LandPrice')
k = 0
for i in result_land:
    
    postedLandPrice = 0
    postedLandPrice_query = i.find('ksj:postedLandPrice')
    postedLandPrice = int(postedLandPrice_query.text)
    
    def extract(name):
        variable = 0
        result = i.find_all('ksj:%s' % name)
        jcount = 0
        for j in result:
            jcount += 1
            if len(result) > 1:
                if jcount == 2:
                    variable = j.text
            elif len(result) > 0:
                variable = j.text
        return variable
    
    cityName = extract('cityName')
    address = extract('address')
    
    currentUse = 0
    currentUse_list = []
    currentUse_result = i.find_all('ksj:currentUse')
    mcount = 0
    for m in currentUse_result:
        mcount += 1
        if len(currentUse_result) > 0:
            if m.text != 'false':
                if m.text != 'true':
                    currentUse_list.append(m.text)
                    currentUse = ','.join(currentUse_list)
        else:
            currentUse = m.text
    
    buildingStructure = extract('buildingStructure')
    waterFacility = extract('waterFacility')
    gasFacility = extract('gasFacility')
    sewageFacility = extract('sewageFacility')
    numberOfFloors = extract('numberOfFloors')
    numberOfBasementFloors = extract('numberOfBasementFloors')
    frontalRoad = extract('frontalRoad')
    widthOfFrontalRoad = extract('widthOfFrontalRoad')
    surroundingPresentUsage = extract('surroundingPresentUsage')
    nameOfNearestStation = extract('nameOfNearestStation')
    distanceFromStation = extract('distanceFromStation')
    useDistrict = extract('useDistrict')
    if not useDistrict:
        useDistrict = extract('restrictionByCityPlanningLaw')
    fireArea = extract('fireArea')
    urbanPlanningArea = extract('urbanPlanningArea')
    
    conn = sqlite3.connect('C:/db/01_land.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO land19 (ID,LAT,LON,POS,PRICE,CITY,ADDR,BLDUSE,STRU,WATER,GAS,SEWAGE,FLUP,FLDOWN,ROAD,ROADW,NEAR,EKI,EKIDIST,DISTUSE,FIRE,PLAN) \
            VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (latitude[k],longitude[k],pos[k],postedLandPrice,cityName,address,currentUse,buildingStructure,waterFacility,gasFacility,sewageFacility,
             numberOfFloors,numberOfBasementFloors,frontalRoad,widthOfFrontalRoad,surroundingPresentUsage,nameOfNearestStation,
             distanceFromStation,useDistrict,fireArea,urbanPlanningArea));
    conn.commit()
    conn.close()
    k += 1