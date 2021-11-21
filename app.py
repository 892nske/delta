import dash  
from dash import dcc 
from dash import html 
import plotly.graph_objects as go
import pandas as pd


app = dash.Dash()

server = app.server


data_spot = pd.read_csv('BTCUSD_spot.csv')
data_perp = pd.read_csv('BTCUSD_perp.csv')

fig = go.Figure()
fig.add_trace(go.Scatter(x=data_spot['timestamp'],
                          y=data_spot['close'],
                          mode='lines',#plotの種類
                          name='spot' #plotの名前
                          ))
                          
fig.add_trace(go.Scatter(x=data_perp['timestamp'],
                          y=data_perp['close'],
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