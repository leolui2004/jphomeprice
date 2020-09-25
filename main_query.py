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
import urllib.parse

mapbox_access_token = ''

# earthquake prob. on map
conn = sqlite3.connect('earthquake.db')
c = conn.cursor()
cursor = c.execute("SELECT ID,LAT,LON,Y30S6 FROM earth2019")
points_earth = {}
for row in cursor:
    points_earth.update({row[0] : (row[1], row[2], row[3])})
points_earth_df = pd.DataFrame.from_dict(points_earth, orient='index', columns=['LAT', 'LON', 'Y30S6'])
conn.close()

#displaying height points on map
def get_height():
    conn = sqlite3.connect('height.db')
    c = conn.cursor()
    cursor = c.execute("SELECT ID,LAT,LON,HEIGHTAVG FROM height2011")
    points_height = {}
    for row in cursor:
        heightavg_transform = row[3] + 0.01 # prevent log error
        points_height.update({row[0] : (row[1], row[2], heightavg_transform)})
    points_height_df = pd.DataFrame.from_dict(points_height, orient='index', columns=['LAT', 'LON', 'HEIGHTAVG'])
    conn.close()
    return points_height_df

conn = sqlite3.connect('street.db')
c = conn.cursor()
cursor = c.execute("SELECT DISTINCT municipal_name FROM streetname")
municipal_name = []
municipal_name_list = []
for row in cursor:
    municipal_name.append({'label':row[0],'value':row[0]})
    municipal_name_list.append(row[0])
conn.close()

def get_street(municipal):
    conn = sqlite3.connect('street.db')
    c = conn.cursor()
    cursor = c.execute("SELECT street_name,street_id FROM streetname WHERE municipal_name=?",(municipal,))
    street_name = []
    street_name_rev = {}
    street_name_list = []
    for row in cursor:
        street_name.append({'label':row[0],'value':row[1]})
        street_name_rev.update({row[1]:row[0]})
        street_name_list.append(row[1])
    conn.close()
    return street_name, street_name_rev, street_name_list

def get_polygon(street_id):
    conn = sqlite3.connect('street.db')
    c = conn.cursor()
    cursor = c.execute("SELECT polygon_lon,polygon_lat FROM polygon WHERE street_id=?",(street_id,))
    polygon = []
    for row in cursor:
        polygon.append([row[0], row[1]])
    conn.close()
    return polygon

def get_land(municipal, street, year):
    conn = sqlite3.connect('landprice.db')
    c = conn.cursor()
    cursor = c.execute("SELECT PRICE FROM '%s' WHERE municipal='%s' AND street='%s'" % (f'land{year}',municipal,street))
    landprice = []
    for row in cursor:
        landprice.append(row[0])
    conn.close()
    return landprice

def get_property(municipal, street):
    conn = sqlite3.connect('homeprice.db')
    c = conn.cursor()
    cursor = c.execute("SELECT pid FROM home WHERE municipal=? AND street=?",(municipal,street,))
    pid = []
    price = []
    pricearea = []
    for row in cursor:
        pid.append(row[0])
        conn = sqlite3.connect('homeprice.db')
        c = conn.cursor()
        cursor = c.execute("SELECT price,pricearea FROM price WHERE pid=?",(row[0],))
        for row in cursor:
            price.append(row[0])
            pricearea.append(row[1])
        conn.close()
    conn.close()
    return pid, price, pricearea

def get_crime(municipal, street, year):
    conn = sqlite3.connect('support.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM '%s' WHERE municipal='%s' AND street='%s'" % (f'crime{year}',municipal,street))
    c_total, c_thug, c_violent, c_intheft, c_theft = [], [], [], [], []
    for row in cursor:
        c_total.append(row[3])
        c_thug.append(row[4])
        c_violent.append(row[5])
        c_intheft.append(row[6])
        c_theft.append(row[7])
    conn.close()
    return c_total, c_thug, c_violent, c_intheft, c_theft

# height points on map
app = dash.Dash(__name__, )
app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.Div([
                dcc.RadioItems(options=[{'label':'地震','value':'earth'},{'label':'高さ','value':'height'},{'label':'街レベル','value':'street'}],
                                        id='div_p',value='earth')],style={'width': '55%'}),
            html.Div(id='margin1', style={'height': 10}),
            html.Div(children=[html.Div(id='div_d1',
                                        children=html.Div([dcc.Dropdown(options=[{'label':'','value':''}],id='select_d1',value='',style={'display':'none'})]))],
                     style={'width': 400}),
            html.Div(id='margin2', style={'height': 10}),
            html.Div(children=[html.Div(id='div_d2',
                                        children=html.Div([dcc.Dropdown(options=[{'label':'','value':''}],id='select_d2',value='',style={'display':'none'})]))],
                     style={'width': 400}),
            html.Div(id='margin3', style={'height': 10}),
            html.Div(html.Button('更新', id='refresh', n_clicks=0), style={'width': 100}),
        ]),
        html.Div(children=[dcc.Graph(id='map', style={'height': 1100})])
    ],style={'width': '55%', 'float': 'left', 'display': 'inline-block'}),
    html.Div([
        html.Div(id='margin4', style={'height': 20}),
        html.H2('詳細情報'),
        html.Div(id='div_street', style={'height': 50}),
        html.H4('現時点'),
        html.Div(id='div_d3', style={'height': 100}),
        html.Div(id='div_d4', style={'height': 100}),
        html.H4('年別'),
        html.Div(children=[dcc.Slider(id='slider', min=2010,max=2020,value=2020,
                                      marks={2010:'2010',2012:'2012',2014:'2014',2016:'2016',2018:'2018',2020:'2020'})]),
        html.Div(dt.DataTable(data=[{'title':'スライドして更新'}], columns=[{'name':'犯罪情報','id':'title'}]), id='div_d5', style={'height': 100}),
        html.H4('平均土地価格'),
        html.Div(children=[dcc.Graph(id='price', style={'height': 400})]),
        html.H2('レポート出力'),
        html.H5('リンクボタンをクリックすると、上記の表をCSVにエクスポートして、ダウンロードします。'),
        html.Div(id='export', style={'height': 100}),
    ],style={'width': '45%', 'float': 'right', 'display': 'inline-block'}),
])

# state record for callback
button = {'refresh':0}
selected = {'select_d1':0,'select_d2':0}
def get_state():
    return button, selected
def reset_selected():
    selected = {'select_d1':0,'select_d2':0}
    return selected

# callback #

@app.callback(
    [Output('map','figure'),Output('div_d1','children'),Output('div_d2','children'),Output('div_d3','children'),
     Output('div_d4','children'),Output('export','children'),Output('price', 'figure'),Output('div_street','children')],
    [Input('refresh','n_clicks'), Input('div_p','value'),Input('select_d1','value'),Input('select_d2','value')])

def update_lp(n_clicks,value1,value2,value3):
    fig = go.Figure()
    children = [html.Div([dcc.Dropdown(options=[{'label':'','value':''}],id='select_d1',value='',style={'display':'none'})])]
    children2 = [html.Div([dcc.Dropdown(options=[{'label':'','value':''}],id='select_d2',value='',style={'display':'none'})])]
    children3a, children3b, children4, children_street = [], [], [], []
    fig_price = go.Figure()
    button, selected = get_state()
    
    if n_clicks > button['refresh']:
    
        if 'earth' in value1:
            fig.add_trace(go.Scattermapbox(
                lat=points_earth_df['LAT'], lon=points_earth_df['LON'], mode='markers', hoverinfo='none', opacity=0.5,
                marker=dict(color=points_earth_df['Y30S6'], size=8, colorscale='Viridis',
                            colorbar=dict(title='30年間6弱', tickvals=[0.1,0.2,0.3], ticktext=['10%','20%','30%'])), text=['Montreal']))
            fig.update_layout(mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=go.layout.mapbox.Center(lat=35.7, lon=139.62),
                                          pitch=0, zoom=10), hovermode='closest', margin=dict(l=20,r=0,b=0,t=20))
            reset_selected()
        
        elif 'height' in value1:
            points_height_df = get_height()
            fig.add_trace(go.Scattermapbox(
                lat=points_height_df['LAT'], lon=points_height_df['LON'], mode='markers', hoverinfo='none', opacity=0.5,
                marker=dict(color=np.log10(points_height_df['HEIGHTAVG']), size=8, colorscale='Viridis',
                            colorbar=dict(title='平均高さ', tickvals=[1,2,3], ticktext=['10m','100m','1000m'])), text=['Montreal']))
            fig.update_layout(mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=go.layout.mapbox.Center(lat=35.7, lon=139.62),
                                          pitch=0, zoom=10), hovermode='closest', margin=dict(l=20,r=0,b=0,t=20))
            reset_selected()
        
        elif 'street' in value1:
            fig.add_trace(go.Scattermapbox())
            fig.update_layout(mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=go.layout.mapbox.Center(lat=35.7, lon=139.62),
                                          pitch=0, zoom=10), hovermode='closest', margin=dict(l=0,r=50,b=0,t=20))
            if selected['select_d1'] == 0:
                children = [html.Div([dcc.Dropdown(options=municipal_name,id='select_d1',value='',style={'display': 'block'})])]
                selected.update({'select_d1':1})
            else:
                if value2 not in municipal_name_list:
                    children = [html.Div([dcc.Dropdown(options=municipal_name,id='select_d1',value='',style={'display': 'block'})])]
                else:
                    children = [html.Div([dcc.Dropdown(options=municipal_name,id='select_d1',value=value2,style={'display': 'block'})])]
                    if selected['select_d2'] == 0:
                        street_name, _, _ = get_street(value2)
                        selected.update({'select_d1':value2})
                        children2 = [html.Div([dcc.Dropdown(options=street_name,id='select_d2',value='',style={'display': 'block'})])]
                        selected.update({'select_d2':1})
                    else:
                        street_name, street_name_rev, street_name_list = get_street(value2)
                        if value3 not in street_name_list:
                            children2 = [html.Div([dcc.Dropdown(options=street_name,id='select_d2',value='',style={'display': 'block'})])]
                        else:
                            children2 = [html.Div([dcc.Dropdown(options=street_name,id='select_d2',value=value3,style={'display': 'block'})])]
                            polygon = get_polygon(value3)
                            
                            fig.update_layout(mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=go.layout.mapbox.Center(lat=35.7, lon=139.62),
                                                          pitch=0, zoom=10, layers=[{'source': {
                                                              'type':"FeatureCollection",'features':[{
                                                                  'type':"Feature", 'geometry':{'type':"MultiPolygon",'coordinates': [[polygon]]}}]},
                                                                  'type':"fill", 'below':"traces", 'color':"royalblue", 'opacity':0.5}]),
                                                          hovermode='closest', margin=dict(l=0,r=50,b=0,t=20))
                            
                            landprice = get_land(value2.replace(' ',''), street_name_rev[value3], 2019)
                            col1 = [{'name':'土地数','id':'no'},{'name':'平均土地価格','id':'mean'},{'name':'最大土地価格','id':'max'},
                                    {'name':'最小土地価格','id':'min'}]
                            if landprice:
                                land_no = len(landprice)
                                land_mean = int(statistics.mean(landprice))
                                land_max = max(landprice)
                                land_min = min(landprice)
                            else:
                                land_no = 'データなし'
                                land_mean = 'データなし'
                                land_max = 'データなし'
                                land_min = 'データなし'
                            dat1 = [{'no':land_no,'mean':land_mean,'max':land_max,'min':land_min}]
                            children3a.append(dt.DataTable(data=dat1, columns=col1))
                            
                            pid, price, pricearea = get_property(value2.replace(' ',''), street_name_rev[value3])
                            col2 = [{'name':'物件数','id':'property'},{'name':'平均価格','id':'avgp'},{'name':'平均平米単価','id':'avgpa'},
                                    {'name':'最大平米単価','id':'maxpa'},{'name':'最小平米単価','id':'minpa'}]
                            if pid:
                                home = len(pid)
                                home_avgp = int(statistics.mean(price))
                                home_avgpa = int(statistics.mean(pricearea))
                                home_maxpa = max(pricearea)
                                home_minpa = min(pricearea)
                            else:
                                home = 'データなし'
                                home_avgp = 'データなし'
                                home_avgpa = 'データなし'
                                home_maxpa = 'データなし'
                                home_minpa = 'データなし'
                            dat2 = [{'property':home,'avgp':home_avgp,'avgpa':home_avgpa,'maxpa':home_maxpa,'minpa':home_minpa}]
                            children3b.append(dt.DataTable(data=dat2, columns=col2))
                            
                            c_total, c_thug, c_violent, c_intheft, c_theft = get_crime(value2.replace(' ',''), street_name_rev[value3], 2019)
                            if c_total:
                                c_total = c_total
                                c_thug = c_thug
                                c_violent = c_violent
                                c_intheft = c_intheft
                                c_theft = c_theft
                            else:
                                c_total = 'データなし'
                                c_thug = 'データなし'
                                c_violent = 'データなし'
                                c_intheft = 'データなし'
                                c_theft = 'データなし'
                            
                            price_x, price_y = [], []
                            for i in range(2010,2020):
                                price_x.append(i)
                                landprice = get_land(value2.replace(' ',''), street_name_rev[value3], i)
                                if landprice:
                                    price_y.append(int(statistics.mean(landprice)))
                                    fig_price.add_trace(go.Scatter(x=price_x, y=price_y, mode='lines', connectgaps=True))
                                    fig_price.update_layout(xaxis_rangeslider_visible=False, showlegend=False)
                            
                            children_street.append(html.H3(f'{value2}{street_name_rev[value3]}'))
                            
                            df = pd.DataFrame({
                                '地名':[f'{value2}{street_name_rev[value3]}'],
                                '土地数':[land_no], '平均土地価格':[land_mean], '最大土地価格':[land_max], '最小土地価格':[land_min],
                                '物件数':[home], '平均価格':[home_avgp], '平均平米単価':[home_avgpa], '最大平米単価':[home_maxpa], '最小平米単価':[home_minpa],
                                '合計_2019':[c_total], '凶悪犯_2019':[c_thug], '粗暴犯_2019':[c_violent],
                                '侵入窃盗_2019':[c_intheft], '非侵入窃盗_2019':[c_theft]
                                })
                            csv_string = df.to_csv(index=False, encoding='utf-8')
                            csv = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
                            children4.append(html.A('エクスポート', id='link', download="data.csv", href=csv, target="_blank" ))
                            
                            selected.update({'select_d1':value2.replace(' ',''), 'select_d2':street_name_rev[value3]})
        
        button.update({'refresh':n_clicks})
        
        return fig, children, children2, children3a, children3b, children4, fig_price, children_street

@app.callback(
    [Output('div_d5','children')],
    [Input('slider','value')])

def update_slider(value4):
    children3c = []
    c_total, c_thug, c_violent, c_intheft, c_theft = get_crime(selected['select_d1'], selected['select_d2'], value4)
    col3 = [{'name':'合計','id':'total'},{'name':'凶悪犯','id':'thug'},{'name':'粗暴犯','id':'violent'},
            {'name':'侵入窃盗','id':'intheft'},{'name':'非侵入窃盗','id':'theft'}]
    if c_total:
        c_total = c_total
        c_thug = c_thug
        c_violent = c_violent
        c_intheft = c_intheft
        c_theft = c_theft
    else:
        c_total = 'データなし'
        c_thug = 'データなし'
        c_violent = 'データなし'
        c_intheft = 'データなし'
        c_theft = 'データなし'
    dat3 = [{'total':c_total,'thug':c_thug,'violent':c_violent,'intheft':c_intheft,'theft':c_theft}]
    children3c.append(dt.DataTable(data=dat3, columns=col3))
    return children3c

#change debug to false after finished development
if __name__ == '__main__':
    app.run_server(debug=False)