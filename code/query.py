import pandas as pd
import numpy as np
import statistics
import sqlite3
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
import plotly.graph_objects as go

island = ['東京大島','新島','神津島','東京三宅','八丈','小笠原']

#map query
#displaying all points on map (land)
conn = sqlite3.connect('C:/db/01_land.db')
c = conn.cursor()
query = f"SELECT ID,LAT,LON,POS,PRICE,ADDR FROM land19 WHERE CITY NOT IN ({','.join(['?']*len(island))})"
cursor = c.execute(query, island)
points_land = {}
for row in cursor:
    #lat = round(row[1],5)
    #lon = round(row[2],5)
    #pos_land = str(lat) + ',' + str(lon)
    addr = row[5][4:].replace("ケ", "ヶ")
    points_land.update({row[0] : (row[1], row[2], row[3], row[4], addr)})
points_land_df = pd.DataFrame.from_dict(points_land, orient='index', columns=['LAT', 'LON', 'POS', 'PRICE', 'ADDR'])
conn.close()

#displaying all points on map (earth)
conn = sqlite3.connect('C:/db/02_earthquake.db')
c = conn.cursor()
cursor = c.execute("SELECT ID,LAT,LON,Y30S6 FROM earth19")
points_earth = {}
for row in cursor:
    points_earth.update({row[0] : (row[1], row[2], row[3])})
points_earth_df = pd.DataFrame.from_dict(points_earth, orient='index', columns=['LAT', 'LON', 'Y30S6'])
conn.close()

#displaying all points on map (height)
conn = sqlite3.connect('C:/db/04_height.db')
c = conn.cursor()
cursor = c.execute("SELECT ID,LAT,LON,HEIGHTAVG FROM height11")
points_height = {}
for row in cursor:
    heightavg_transform = row[3] + 1 #prevent log error
    points_height.update({row[0] : (row[1], row[2], heightavg_transform)})
points_height_df = pd.DataFrame.from_dict(points_height, orient='index', columns=['LAT', 'LON', 'HEIGHTAVG'])
conn.close()

mapbox_access_token = ''

#display
app = dash.Dash(__name__, )
app.layout = html.Div(children=[
    html.Div([
        html.Div([
                dcc.RadioItems(options=[{'label':'Price','value':'price'}, {'label':'Earthquake Prob.','value':'earth'},
                                       {'label':'Height','value':'height'}], id='layer', value='price', labelStyle={'display':'inline-block'})]),
        html.Div(children=[
                dcc.Graph(id='map', style={'height': 1200})])
    ],style={'width': '55%', 'float': 'left', 'display': 'inline-block'}),
    html.Div([
        html.Div(id='margin1', style={'height': 50}),
        html.H3('Price Information for Selected Points by Box or Lasso'),
        html.Div(children=[dcc.Slider(id='cross-stat-slider', min=1983,max=2019,value=2018,
                                      marks={1983:'1983',1990:'1990',2000:'2000',2010:'2010',2019:'2019'})]),
        html.Div(id='cross-stat', style={'height': 100}),
        html.Div(id='margin2', style={'height': 50}),
        html.H3('Price Information for Selected Point by Click'),
        html.Div(children=[
                dcc.Graph(id='drill-price', style={'height': 400})]),
        html.H3('All Information for Selected Point by Click'),
        html.Div(children=[dcc.Slider(id='drill-price-slider', min=1983,max=2019,value=2018,
                                      marks={1983:'1983',1990:'1990',2000:'2000',2010:'2010',2019:'2019'})]),
        html.Div(id='drill-info1', style={'height': 80}),
        html.Div(id='drill-info2', style={'height': 80}),
        html.Div(id='drill-info3', style={'height': 80}),
        html.Div(id='drill-info4', style={'height': 80}),
    ],style={'width': '45%', 'float': 'right', 'display': 'inline-block'}),
])

@app.callback(
    Output('map', 'figure'),
    [Input('layer', 'value')])

def update_output(value):
    fig = go.Figure()
    if 'price' in value:
        fig.add_trace(go.Scattermapbox(lat=points_land_df['LAT'], lon=points_land_df['LON'],
            hovertext=points_land_df['ADDR'], hoverinfo='text', mode='markers', customdata=points_land_df['POS'],
            opacity=0.7, marker=dict(color=np.log10(points_land_df['PRICE']), size=8, colorscale='Viridis',
                                     colorbar=dict(title='PRICE', tickvals=[4,5,6,7], ticktext=['10K','100K','1M','10M'])), text=['Montreal']))
        fig.update_layout(mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=go.layout.mapbox.Center(lat=35.7, lon=139.62),
                                      pitch=0, zoom=10), hovermode='closest', margin=dict(l=20,r=0,b=0,t=20))
        return fig
    if 'earth' in value:
        fig.add_trace(go.Scattermapbox(
            lat=points_earth_df['LAT'], lon=points_earth_df['LON'], mode='markers', hoverinfo='none', opacity=0.5,
            marker=dict(color=points_earth_df['Y30S6'], size=8, colorscale='Viridis',
                        colorbar=dict(title='6+ in 30yrs', tickvals=[0.1,0.2,0.3], ticktext=['10%','20%','30%'])), text=['Montreal']))
        fig.update_layout(mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=go.layout.mapbox.Center(lat=35.7, lon=139.62),
                                      pitch=0, zoom=10), hovermode='closest', margin=dict(l=20,r=0,b=0,t=20))
        return fig
    if 'height' in value:
        fig.add_trace(go.Scattermapbox(
            lat=points_height_df['LAT'], lon=points_height_df['LON'], mode='markers', hoverinfo='none', opacity=0.5,
            marker=dict(color=np.log10(points_height_df['HEIGHTAVG']), size=8, colorscale='Viridis',
                        colorbar=dict(title='Average Height', tickvals=[1,2,3], ticktext=['10m','100m','1000m'])), text=['Montreal']))
        fig.update_layout(mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=go.layout.mapbox.Center(lat=35.7, lon=139.62),
                                      pitch=0, zoom=10), hovermode='closest', margin=dict(l=20,r=0,b=0,t=20))
        return fig

@app.callback(
    Output('cross-stat', 'children'),
    [Input('map', 'selectedData'),
     Input('cross-stat-slider', 'value')])

def cross_output(selectedData, value):
    if selectedData is None:
        requestid_cross = ['35.67182,139.76522']
    else:
        requestid_cross = [i['customdata'] for i in selectedData['points']]
    
    value_str = str(value)
    crossyear_query_slider = 'land{}'.format(value_str[2:])
    crossprice = []
    for i in range(len(requestid_cross)):
        conn = sqlite3.connect('C:/db/01_land.db')
        c = conn.cursor()
        cursor = c.execute("SELECT PRICE FROM '%s' WHERE POS = '%s'" % (crossyear_query_slider, requestid_cross[i]))
        results = cursor.fetchone()
        if results is not None:
            crossprice.append(results[0])
        conn.close()
    if len(requestid_cross) == 1:
        if crossprice:
            mean_cross = results[0]
            max_cross = results[0]
            min_cross = results[0]
        else:
            mean_cross = 'No Data'
            max_cross = 'No Data'
            min_cross = 'No Data'
    else:
        if crossprice:
            mean_cross = int(statistics.mean(crossprice))
            max_cross = max(crossprice)
            min_cross = min(crossprice)
        else:
            mean_cross = 'No Data'
            max_cross = 'No Data'
            min_cross = 'No Data'
    columns_cross = [{'name':'Year', 'id':'year'},{'name':'AVG Price', 'id':'pavg'},{'name':'MAX Price', 'id':'pmax'},{'name':'MIN Price', 'id':'pmin'}]
    data_cross = [{'year':value, 'pavg':mean_cross, 'pmax':max_cross, 'pmin':min_cross}]
    return dt.DataTable(data=data_cross, columns=columns_cross)

@app.callback(
    Output('drill-price', 'figure'),
    [Input('map', 'clickData')])

def drillprice_output(clickData):
    if clickData is None:
        requestpos = '35.67182,139.76522'
    else:
        requestpos = clickData['points'][0]['customdata']
    
    drillyear = []
    drillprice = []
    for i in range(1983,2020):
        drillyear.append(i)
        drillyear_str = str(i)
        drillyear_query = 'land{}'.format(drillyear_str[2:])
        
        conn = sqlite3.connect('C:/db/01_land.db')
        c = conn.cursor()
        cursor = c.execute("SELECT PRICE FROM '%s' WHERE POS = '%s'" % (drillyear_query, requestpos))
        results = cursor.fetchone()
        if not results:
            results = 'NaN'
        drillprice.append(results[0])
        conn.close()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=drillyear, y=drillprice, mode='lines', connectgaps=True))
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

@app.callback(
    [Output('drill-info1', 'children'),
    Output('drill-info2', 'children'),
    Output('drill-info3', 'children'),
    Output('drill-info4', 'children')],
    [Input('map', 'clickData'),
     Input('drill-price-slider', 'value')])

def drillinfo_output(clickData, value):
    if clickData is None:
        requestpos = '35.67182,139.76522'
    else:
        requestpos = clickData['points'][0]['customdata']
    
    value_str = str(value)
    drillyear_land_slider = 'land{}'.format(value_str[2:])
    drillyear_train_slider = 'train{}'.format(value_str[2:])
    drillyear_crime_slider = 'crime{}'.format(value_str[2:])
    col1 = [{'name':'Year', 'id':'year'},{'name':'Price', 'id':'price'},{'name':'Address', 'id':'addr'},{'name':'Use', 'id':'use'},
            {'name':'Structure', 'id':'structure'},{'name':'Water', 'id':'water'},{'name':'Gas', 'id':'gas'},{'name':'Sewage', 'id':'sewage'},
            {'name':'Floor', 'id':'floor'},{'name':'Basement', 'id':'basement'}]
    col2 = [{'name':'Road', 'id':'road'},{'name':'Road Width', 'id':'width'},{'name':'Nearby', 'id':'nearby'},{'name':'District Use', 'id':'distuse'},
            {'name':'Fire Resistant', 'id':'fire'},{'name':'City Planning', 'id':'plan'}]
    col3 = [{'name':'Nearest Station', 'id':'station'},{'name':'Train Line', 'id':'stationline'},{'name':'Train Company', 'id':'stationcomp'},
            {'name':'Station Distant', 'id':'distant'}]
    col4 = [{'name':'Crime Total', 'id':'crimet'},{'name':'Violent Crime', 'id':'violent'},{'name':'Invasion Theft', 'id':'intheft'},
            {'name':'Theft', 'id':'theft'}]
    
    conn = sqlite3.connect('C:/db/01_land.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM '%s' WHERE POS = '%s'" % (drillyear_land_slider, requestpos))
    results = cursor.fetchone()
    conn.close()
    
    try:
        if results[17]:
            if results[17] != '0':
                conn = sqlite3.connect('C:/db/03_train.db')
                c = conn.cursor()
                cursor = c.execute("SELECT * FROM '%s' WHERE EKINAME = '%s'" % (drillyear_train_slider, results[17]))
                results_train = cursor.fetchone()
                conn.close()
            else:
                results_train = ('No Data','No Data','No Data','No Data','No Data')
        else:
            results_train = ('No Data','No Data','No Data','No Data','No Data')
    except Exception:
        results_train = ('No Data','No Data','No Data','No Data','No Data')
    
    try:
        conn = sqlite3.connect('C:/db/05_crime.db')
        c = conn.cursor()
        cursor = c.execute("SELECT ID,ADDRESS FROM '%s'" % drillyear_crime_slider)
        street_dict = {}
        for row in cursor:
            row_replace = row[1].replace("ケ", "ヶ")
            if row_replace[-2:] == '丁目':
                street_dict.update({row_replace[:-2] : row[0]})
            else:
                street_dict.update({row_replace : row[0]})
        conn.close()
        street_query = results[6][4:].replace("ケ", "ヶ")
        street_find1 = street_query.find('－')
        street_find2 = street_query.find('丁目')
        try:
            if street_find1 > -1:
                street_find1_ex = street_query[street_find1+1:]
                if street_find1_ex.find('－') > -1:
                    street_id = street_dict[street_query[:street_find1]]
                else:
                    for i in street_dict:
                        street_find_ex = street_query.find(i)
                        if street_find_ex > -1:
                            street_id = street_dict[i]
            elif street_find2 > -1:
                street_id = street_dict[street_query[:street_find2]]
            else:
                for i in street_dict:
                    street_find_ex = street_query.find(i)
                    if street_find_ex > -1:
                        street_id = street_dict[i]
            conn = sqlite3.connect('C:/db/05_crime.db')
            c = conn.cursor()
            cursor = c.execute("SELECT * FROM '%s' WHERE ID = '%s'" % (drillyear_crime_slider, street_id))
            results_crime = cursor.fetchone()
            conn.close()
        except Exception:
            results_crime = ('No Data','No Data','No Data','No Data','No Data','No Data')
    except Exception:
        results_crime = ('No Data','No Data','No Data','No Data','No Data','No Data')
    
    if not results:
        replace = ('No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data',
                    'No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data','No Data',
                    'No Data','No Data','No Data')
    else:
        replace = results
    dat1 = [{'year':value_str,'price':replace[4],'addr':replace[6],'use':replace[7],'structure':replace[8],
             'water':replace[9],'gas':replace[10],'sewage':replace[11],'floor':replace[12],'basement':replace[13]}]
    dat2 = [{'road':replace[14],'width':replace[15],'nearby':replace[16],'distuse':replace[19],'fire':replace[20],'plan':replace[21]}]
    dat3 = [{'station':replace[17],'stationline':results_train[3],'stationcomp':results_train[4],'distant':replace[18]}]
    dat4 = [{'crimet':results_crime[2],'violent':results_crime[3],'intheft':results_crime[4],'theft':results_crime[5]}]
    return dt.DataTable(data=dat1, columns=col1),dt.DataTable(data=dat2, columns=col2),dt.DataTable(data=dat3, columns=col3),dt.DataTable(data=dat4, columns=col4)

#change debug to false after finished development
if __name__ == '__main__':
    app.run_server(debug=True)