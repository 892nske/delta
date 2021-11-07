import dash  
import dash_core_components as dcc 
import dash_html_components as html  
import plotly.graph_objects as go
import pandas as pd


app = dash.Dash(__name__)

data_btcusdt = pd.read_csv('BTCUSDT.csv')
data_btcusd = pd.read_csv('BTCUSD_SPOT.csv')

fig = go.Figure()
fig.add_trace(go.Scatter(x=data_btcusdt['timestamp'],
                          y=data_btcusdt['cl'],
                          mode='lines',#plotの種類
                          name='BTCUSDT' #plotの名前
                          ))
                          
fig.add_trace(go.Scatter(x=data_btcusd['timestamp'],
                          y=data_btcusd['close'],
                          mode='lines',#plotの種類
                          name='BTCUSD_SPOT' #plotの名前
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