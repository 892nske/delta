import dash  
from dash import dcc 
from dash import html 
import plotly.graph_objects as go
import pandas as pd
import psycopg2


app = dash.Dash()

server = app.server


# 接続情報
connection_config = {
    'host': 'rdsnske.c7sczatjnphy.ap-northeast-1.rds.amazonaws.com',
    'port': '5432',
    'database': 'bot',
    'user': 'rdsuser',
    'password': 'rds%5678'
}

# 接続
connection = psycopg2.connect(**connection_config)

# DataFrameでロード
data_spot = pd.read_sql(sql="SELECT * FROM bybit_api_spot where symbol = 'BTCUSDT';", con=connection )
data_perp = pd.read_sql(sql="SELECT * FROM bybit_api_futures where symbol = 'BTCUSDT';", con=connection )

# data_spot = pd.read_csv('BTCUSD_spot.csv')
# data_perp = pd.read_csv('BTCUSD_perp.csv')

fig = go.Figure()
fig.add_trace(go.Scatter(x=data_spot['basetime'],
                          y=data_spot['last'],
                          mode='lines',#plotの種類
                          name='spot' #plotの名前
                          ))
                          
fig.add_trace(go.Scatter(x=data_perp['basetime'],
                          y=data_perp['last_price'],
                          mode='lines',#plotの種類
                          name='perp' #plotの名前
                          ))

# appという箱に中身を詰める②
app.layout = html.Div(
   children =[
    html.H1('Hello Dash',),
    dcc.Graph(
        figure=fig
    )
])

# 実行用③
if __name__=='__main__':
    app.run_server(debug=True)