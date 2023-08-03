from dash import dcc, html

layout = html.Div([
    html.Div([
        html.H1("Dollar Cost Averaging Strategies", style={
                'textAlign': 'center', 'marginBottom': 50, 'marginTop': 25, 'color': '#2C3E50'}),
    ]),

    html.Div([
        html.Div([
            html.Label("Select Start Date:", style={'font-weight': 'bold'}),
            dcc.DatePickerSingle(
                id='date-picker-start',
                min_date_allowed='2000-01-01',
                max_date_allowed='2023-07-01',
                initial_visible_month='2020-01-01',
                date='2020-01-01'
            ),
            html.Label("Select End Date:", style={'marginTop': 20, 'font-weight': 'bold'}),
            dcc.DatePickerSingle(
                id='date-picker-end',
                min_date_allowed='2000-01-01',
                max_date_allowed='2023-07-01',
                initial_visible_month='2023-01-01',
                date='2023-01-01'
            ),
            dcc.Dropdown(
                id='dropdown-stock',
                options=[
                    {'label': 'Apple', 'value': 'AAPL'},
                    {'label': 'Microsoft', 'value': 'MSFT'},
                    {'label': 'Amazon', 'value': 'AMZN'},
                    {'label': 'S&P 500', 'value': '^GSPC'},
                    {'label': 'Google', 'value': 'GOOGL'},
                    {'label': 'Facebook', 'value': 'FB'},
                    {'label': 'Tesla', 'value': 'TSLA'},
                    {'label': 'Nasdaq Composite', 'value': '^IXIC'},
                    {'label': 'Dow Jones Industrial Average', 'value': '^DJI'},
                    {'label': 'Russell 2000', 'value': '^RUT'},
                    {'label': 'Bitcoin', 'value': 'BTC-USD'},
                    {'label': 'Ethereum', 'value': 'ETH-USD'},
                    {'label': 'Vanguard Total Stock Market ETF', 'value': 'VTI'},
                    {'label': 'Vanguard S&P 500 ETF', 'value': 'VOO'},
                    {'label': 'iShares Russell 2000 ETF', 'value': 'IWM'},
                    {'label': 'SPDR Dow Jones Industrial Average ETF', 'value': 'DIA'},
                    # ... you can continue to add more stocks or funds as needed
                ],
                value='^GSPC',  # Default value
                multi=False,   # Only allow one stock to be selected at a time
                style={'width': '90%', 'marginTop': 20}
            )

        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

        html.Div([
            html.Label("Lump Sum Amount (£):", style={'font-weight': 'bold'}),
            dcc.Input(id="input-lumpsum", type="number", placeholder="Enter Lump Sum Amount", value=10000, style={
                      'width': '90%'}),
            html.Label("Select Frequencies to Compare:", style={'marginTop': 20, 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='dropdown-frequency',
                options=[
                    {'label': 'Lump Sum', 'value': 'lumpsum'},
                    {'label': 'Monthly', 'value': 'monthly'},
                    {'label': 'Biweekly', 'value': 'biweekly'},
                    {'label': 'Weekly', 'value': 'weekly'}
                ],
                value=['monthly', 'weekly'],
                multi=True,
                style={'width': '90%'}
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': 20, 'padding': '10px'}),
    ], style={'marginTop': 20, 'marginBottom': 30, 'backgroundColor': '#ECF0F1', 'borderRadius': '15px', 'padding': '20px'}),

    html.Div([
        dcc.Graph(id='graph-strategy', style={'height': '600px'}),
    ], style={'marginTop': 50, 'boxShadow': '2px 5px 5px 1px rgba(0, 0, 0, 0.2)'}),

    # Here is where we'll display the net profit table:
    html.Div(id='net-profit-display', style={
             'marginTop': 20, 'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ECF0F1', 'borderRadius': '15px'}),

], style={'padding': '20px', 'fontFamily': 'Arial', 'backgroundColor': '#F7F9FA'})
