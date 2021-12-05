import dash  
from dash import dcc 
from dash import html 
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    dcc.Graph(id="btc_graph")
])

@app.callback(
    Output("btc_graph", "figure"),
    [Input("submit-button", 'n_clicks')]
)
def update_output(n_clicks):
    # DataFrameでロード
    data_spot = pd.read_sql(sql="select * from (select * from bybit_api_spot where symbol = 'BTCUSDT' order by create_dt desc limit 60*10) d order by d.basetime;", con=connection )
    data_perp = pd.read_sql(sql="select * from (select * from bybit_api_futures where symbol = 'BTCUSDT' order by create_dt desc limit 60*10) d order by d.basetime;", con=connection )

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=("price", "dif"),
        vertical_spacing=0.1,
        row_heights = [3, 1]
    )
    fig.add_trace(go.Scatter(x=data_spot['basetime'],
                          y=data_spot['last'],
                          mode='lines',#plotの種類
                          name='spot' #plotの名前
    ),row=1, col=1)
    fig.add_trace(go.Scatter(x=data_perp['basetime'],
                          y=data_perp['last_price'],
                          mode='lines',#plotの種類
                          name='perp' #plotの名前
    ),row=1, col=1)
    fig.add_trace(go.Scatter(x=data_perp['basetime'],
                          y=data_perp['last_price']/data_spot['last']-1,
                          mode='lines',#plotの種類
                          name='dif' #plotの名前
    ),row=2, col=1)
    fig.update_layout(height=800, width=1300)

    return fig


# 実行用
if __name__=='__main__':
    app.run_server(debug=True)