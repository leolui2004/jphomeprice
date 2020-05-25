# Try to use Python Plotly and Dash to display land price information in Tokyo
My first project on github. Using Plotly and Dash to create an interactive dashboard. As I just want to test the function so I did not do too much for the layout and the form of information presentation.

## Function
* A first layer on the map showing land price over thousands of places in Tokyo
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/query1.png)
* A second layer on the map showing earthquake probability in Tokyo
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/query2.png)
* A third layer on the map showing average height of a grid of land in Tokyo
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/query3.png)
**Drill down**
* A graph showing price information of that land by clicking a point on the map
* A table showing other relative information (e.g. nearest train station, crimes) of that land by clicking a point on the map
* A slider which can show information in different record years
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/query4.png)
**Cross Filter**
* A table showing average, highest, lowest land price of selected points by selecting points using box or lasso tool
* A slider which can show information in different record years
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/query5.png)

## Methodology
### Data Processing Part
1. Download data from different websites
2. Extract data (mainly xml and csv, so Beautiful Soup and Pandas are used)
3. Make necessary necessary transformation or data cleansing (e.g. Transform mesh code to coordinate)
4. Store the data to sqlite database
### Presentation Part
5. Create a Dash and Plotly basic layout
6. Make a query request and display the data points on a map using Plotly Scattermapbox
7. Create a radio item callback for switching layers on the map
8. Create a callback when selected one point(by click) on the map, showing price graph and table of relative information
9. Create a callback when selected one or multiple points on the map, showing average, highest, lowest land price
10. Create slider callbacks for #5 and #6 which can choose different record years

## Data Source and References
1. Land price and other relative information - [地価公示](http://nlftp.mlit.go.jp/ksj/)
2. Earthquake probability - [地震ハザードステーション](http://www.j-shis.bosai.go.jp/download)
3. Train station information - [鉄道](http://nlftp.mlit.go.jp/ksj/)
4. Height information - [標高・傾斜度5次メッシュ](http://nlftp.mlit.go.jp/ksj/)
5. Crime information - [認知件数](https://www.keishicho.metro.tokyo.jp/about_mpd/jokyo_tokei/jokyo/)
6. Reference for transforming between mesh code and coordinate [算出方法](http://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf#page=13)
