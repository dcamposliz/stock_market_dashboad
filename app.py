import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash()

app.layout = html.Div(children=[
    
    # header
    html.H1('Stock Ticker Dashboard'),
    
    # call to action
    html.H3('Enter a stock symbol:'),
    
    # stock input
    dcc.Input(
        id='my_stock_picker',
        value='TSLA',
    ),
    
    # stock output: graph
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y':[3,1]}
            ],
            'layout': {
                'title': 'Default Title'
            },
        }
    )
])

@app.callback(Output('my_graph','figure'), [Input('my_stock_picker', 'value')])
def update_graph(stock_ticker):
    fig = {
        'data': [{'x': [1,2], 'y':[3,1]}],
         'layout': {'title': stock_ticker}
    }
    return fig

if __name__ == '__main__':
    app.run_server()