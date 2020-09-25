# Python Plotly and Dash for Dashboard Visualization Demonstration
My nineth project on github, or basically a full revision for my first project. Using Plotly and Dash to create an interactive dashboard visualization showing land price and home price and other related information in Tokyo. As I just want to test the function so I did not do too much for the layout.

Feel free to provide comments, I am now concentrating on data anylysis and web presentation.

## Function
* A first layer on the map showing earthquake probability in Tokyo
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/01.gif)

* A second layer on the map showing average height of a grid of land in Tokyo
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/02.gif)

* A third layer on the map showing the shape of the selected place in Tokyo with more relevant information on right side
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/03.gif)

* Enlarged image of the area filled

![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/01.png)

* A slider refresh on slide providing information by different years
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/04.gif)

* A link button that can download the data shown on above table in a CSV format
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/05.gif)

## Methodology
### Data Processing
I downloaded data from the web and stored it to database, pre-processing is needed for example some place name are not identical in different sources, with some numbers in fullwidth (e.g. １, 1), place name with a little bit difference (e.g. ヶ, ケ), etc. However as the data processing part is not the main focus of this project, I will skip mentioning detail about that.

### Visualization
There are many ways to perform multi-input, multi-output on Plotly and Dash, but for easier overall funtion management, I used 
1. a refresh button for switching map layers and choosing item from dropdown menus
2. dictionaries to store the state of button and dropdown menu thus more flexible on controlling those objects
3. a separate callback for slider so that just slide and show the new data, no refresh button is needed

And the layers are
1. earthquake probability for next 30 years
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/02.png)

2. average height
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/03.png)

3. land price, home price, crime information on selected place
![image](https://github.com/leolui2004/jphomeprice/blob/master/picture/04.png)

## Data Source and References
1. Land price and other relative information - [地価公示](http://nlftp.mlit.go.jp/ksj/)
2. Earthquake probability - [地震ハザードステーション](http://www.j-shis.bosai.go.jp/download)
3. Train station information - [鉄道](http://nlftp.mlit.go.jp/ksj/)
4. Height information - [標高・傾斜度5次メッシュ](http://nlftp.mlit.go.jp/ksj/)
5. Crime information - [認知件数](https://www.keishicho.metro.tokyo.jp/about_mpd/jokyo_tokei/jokyo/)
6. Reference for transforming between mesh code and coordinate [算出方法](http://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf#page=13)
