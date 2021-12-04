import dash  
from dash import dcc 
from dash import html 
from dash.dependencies import Input, Output, State
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


# appという箱に中身を詰める②
app.layout = html.Div([
    html.Button(id="submit-button", children="表示"),
    dcc.Graph(id="price_graph")
])

@app.callback(
    Output("price_graph", "figure"),
    [Input("submit-button", 'n_clicks')]
)
def update_output(n_clicks):
    # DataFrameでロード
    data_spot = pd.read_sql(sql="select * from (select * from bybit_api_spot where symbol = 'BTCUSDT' order by create_dt desc limit 60*100) d order by d.basetime;", con=connection )
    data_perp = pd.read_sql(sql="select * from (select * from bybit_api_futures where symbol = 'BTCUSDT' order by create_dt desc limit 60*100) d order by d.basetime;", con=connection )

    fig = go.Figure(layout=go.Layout(
                title = 'BTC',
                height = 800, 
                width = 1300,
                xaxis = dict(title="時刻"),
                yaxis = dict(title="価格")
    ))
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

    return fig


# 実行用③
if __name__=='__main__':
    app.run_server(debug=True)