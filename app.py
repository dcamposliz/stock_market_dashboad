import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime
import pandas as pd

app = dash.Dash()

nsdq = pd.read_csv('data/nasdaq_company_list.csv')
nsdq.set_index('Symbol', inplace = True)

options = [

]

for tic in nsdq.index:
    mydict = {}
    mydict['label'] = nsdq.loc[tic]['Name'] + ' (' + tic + ')'
    mydict['value'] = tic
    options.append(mydict)

app.layout = html.Div(children = [
    
    # header
    html.H1('Stock Ticker Dashboard'),

    # body
    html.Div(
        children = [
            # call to action
            html.H3('Enter a stock symbol:', style = {'paddingRight': '30px'}),

            # stock input
            dcc.Dropdown(
                id = 'my_ticker_symbol',
                options = options,
                value = ['TSLA', 'GOOG', 'MSFT', 'AMZN'],
                multi = True
            )
        ],
        style = {
            'display':'inline-block',
            'verticalAlign': 'top',
            'width': '30%'
        }
    ),

    html.Div(
        children = [
            html.H3('Select a start and end date:'),
            dcc.DatePickerRange(
                id = 'my_date_picker',
                
                min_date_allowed = datetime(2015, 1, 1),
                max_date_allowed = datetime.today(),
                
                start_date = datetime(2018, 1, 1),
                end_date = datetime.today(),
                
                clearable=True,
            )
        ],
        style = {'display':'inline-block'}
    ),

    # submit button
    html.Div(
        children = [
            html.Button(
                id = 'submit-button',
                n_clicks = 0,
                children = 'Submit',
                style = {'fontSize':24, 'marginLeft':'30px'}
            )
        ],
        style={'display': 'inline-block'}
    ),
    
    # stock output: graph
    dcc.Graph(
        id = 'my_graph',
        figure = {
            'data': [
                {'x': [1,2], 'y':[3,1]}
            ],
            'layout': {
                'title': 'Default Title'
            },
        }
    )
])

@app.callback(
    Output('my_graph','figure'),
    [Input('submit-button', 'n_clicks')],
    [
        State('my_ticker_symbol', 'value'),
        State('my_date_picker', 'start_date'),
        State('my_date_picker', 'end_date')
    ]
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):

    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []

    for tic in stock_ticker:
        df = web.DataReader(tic, 'yahoo', start, end)
        traces.append({'x': df.index, 'y': df['Close'], 'name':tic})
    
    print(df.head())
    
    fig = {
        'data': traces,
        'layout': {'title': stock_ticker}
    }
    return fig

if __name__ == '__main__':
    app.run_server()