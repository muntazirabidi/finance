from config import dbc, dcc, html, yf, pd
from dash.dash_table.Format import Group
from dash_table import DataTable

DataTable(
    id='fund-info-table',
    columns=[{"name": i, "id": i} for i in ['Metric', 'Value']],
    data=[]
)

# Define the descriptions with bold headings and professional font styling
investment_description = html.Div([
    html.Strong("Investment Growth:"),
    #html.Br(),
    " This plot shows the growth of an initial investment of GBP 1000 over the selected time frame for the chosen funds."
], style={'fontFamily': 'Helvetica, Arial, sans-serif', 'fontSize': '13px'})

returns_description = html.Div([
    html.Strong("Returns in Percentage:"),
    #html.Br(),
    " Displays the returns in percentage over the selected time frame for the chosen funds."
], style={'fontFamily': 'Helvetica, Arial, sans-serif', 'fontSize': '13px'})

correlation_description = html.Div([
    html.Strong("Correlation Matrix:"),
    #html.Br(),
    " A matrix showcasing how the returns of the selected funds move in relation to one another. A value close to 1 indicates a strong positive correlation, while a value close to -1 indicates a strong negative correlation."
], style={'fontFamily': 'Helvetica, Arial, sans-serif', 'fontSize': '13px'})

volatility_description = html.Div([
    html.Strong("Rolling Volatility:"),
    #html.Br(),
    " This plot illustrates the rolling volatility (standard deviation of returns) of the selected funds over a specified window of days."
], style={'fontFamily': 'Helvetica, Arial, sans-serif', 'fontSize': '13px'})

sharpe_description = html.Div([
    html.Strong("Sharpe Ratio:"),
    #html.Br(),
    " The Sharpe ratio measures the performance of an investment compared to a risk-free asset, after adjusting for its risk. A higher Sharpe ratio indicates better risk-adjusted performance."
], style={'fontFamily': 'Helvetica, Arial, sans-serif', 'fontSize': '13px'})

def fetch_fund_info(ticker):
    """
    Fetches specific information about a fund based on its ticker.

    Parameters:
    - ticker (str): The ticker symbol of the fund.

    Returns:
    - dict: A dictionary containing the desired information about the fund.
    """
    stock = yf.Ticker(ticker)
    
    try:
        info = stock.info
        fund_info = {
            '52-week High': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52-week Low': info.get('fiftyTwoWeekLow', 'N/A'),
            'Dividend Yield': info.get('dividendYield', 'N/A'),
            'Beta': info.get('beta', 'N/A'),
            '200-day Moving Average': info.get('twoHundredDayAverage', 'N/A'),
            '50-day Moving Average': info.get('fiftyDayAverage', 'N/A')
        }
        return fund_info
    except Exception as e:
        print(f"Error fetching info for {ticker}: {e}")
        return {}



# Define the app layout with enhanced styling
layout = dbc.Container([
    html.H1("Index Funds Comparison", style={
        'textAlign': 'center',
        'marginBottom': '40px',
        'marginTop': '20px',
        'color': '#2C3E50',
        'fontFamily': "'Helvetica Neue', Arial, sans-serif",
        'fontWeight': '600',
        'fontSize': '2.2em',
        'background': '#F4F4F4',
        'padding': '10px 15px',
        'borderRadius': '8px',
        'boxShadow': '0px 0px 8px rgba(0, 0, 0, 0.05)'
    }),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Label("Select Fund:", style={'color': '#2C3E50', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='fund-dropdown',
                        options=[
                            {'label': 'US Stock Market Fund', 'value': 'US STOCK MARKET'},
                            {'label': 'Russell 2000', 'value': 'RUSSELL_2000'},
                            {'label': 'Small Cap Funds', 'value': 'SMALL_CAP'},
                            {'label': 'Mid Cap Funds', 'value': 'MID_CAP'},
                            {'label': 'Nasdaq100', 'value': 'NASDAQ100'},
                            {'label': 'S&P500 VOO', 'value': 'S&P500 VOO'},
                            {'label': 'S&P500 VUSA', 'value': 'S&P500 VUSA'},
                            {'label': 'FTSE All-World ETF', 'value': 'FTSE All-World ETF'},
                            {'label': 'FTSE All-World High Dividend', 'value': 'FTSE All-World High Dividend'},
                            {'label': 'Vertex Pharma', 'value': 'Vertex Pharma'},
                            {'label': 'FTSE 100 ETF', 'value': 'FTSE 100 ETF'},
                            {'label': 'Bitcoin GBP', 'value': 'Bitcoin GBP'},
                            {'label': 'ETH GBP', 'value': 'ETH GBP'},
                            {'label': 'Total Bond Market', 'value': 'TOTAL BOND MARKET'},
                            {'label': 'International Stock Index', 'value': 'INTERNATIONAL STOCK INDEX'},
                            {'label': 'Emerging Markets Stock Index', 'value': 'EMERGING MARKETS STOCK INDEX'},
                            {'label': 'Total World Stock ETF', 'value': 'TOTAL WORLD STOCK ETF'},
                            {'label': 'Real Estate ETF', 'value': 'REAL ESTATE ETF'},
                            {'label': 'Total Corporate Bond ETF', 'value': 'TOTAL CORPORATE BOND ETF'},
                            {'label': 'MSCI Emerging Markets', 'value': 'MSCI Emerging Markets'},
                            {'label': 'MSCI EAFE', 'value': 'MSCI EAFE'},
                            {'label': 'Core U.S. Aggregate Bond', 'value': 'Core U.S. Aggregate Bond'},
                            {'label': 'iBoxx $ Investment Grade Corporate Bond', 'value': 'iBoxx $ Investment Grade Corporate Bond'},
                            {'label': 'U.S. Real Estate', 'value': 'U.S. Real Estate'},
                            {'label': 'Russell 1000 Growth', 'value': 'Russell 1000 Growth'},
                            {'label': 'iShares S&P 500 (USD/Accm)', 'value': 'iShares S&P 500 (USD/Accm)'},
                            {'label': 'iShares S&P 500 GBP Dist', 'value': 'iShares S&P 500 GBP Dist'},
                            {'label': 'iShares S&P 500 (Hedged/GBP/Dist)', 'value': 'iShares S&P 500 (Hedged/GBP/Dist)'}


                        ],
                        value=['S&P500 VUSA', 'NASDAQ100'],
                        multi=True,
                         className="mb-3"
                    ),
                    dbc.Label("Select Time Frame:", style={'color': '#2C3E50', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='time-frame-dropdown',
                        options=[
                            {'label': '1 Day', 'value': '1D'},
                            {'label': '5 Days', 'value': '5D'},
                            {'label': '1 Month', 'value': '1M'},
                            {'label': '1 Year', 'value': '1Y'},
                            {'label': '3 Years', 'value': '3Y'},
                            {'label': '5 Years', 'value': '5Y'},
                            {'label': '10 Years', 'value': '10Y'}
                        ],
                        value='1Y',
                        clearable=False,
                        className="mb-3"
                    ),

                    dbc.Label("Select Rolling Volatility Window:", style={'color': '#2C3E50'}),
                    dcc.Dropdown(
                        id='volatility-window-dropdown',
                        options=[
                            {'label': '5-Day Rolling Volatility', 'value': '5D'},
                            {'label': '10-Day Rolling Volatility', 'value': '10D'},
                            {'label': '30-Day Rolling Volatility', 'value': '30D'}
                        ],
                        value='30D',
                        clearable=False,
                        className="mb-3"
                    ),


                dbc.Col([
                    # ... [Your existing dropdown components]

                # Add the descriptions below the dropdowns:
                    investment_description,
                    html.P(style={'margin': '10px 0'}),  # Spacer
                    returns_description,
                    html.P(style={'margin': '10px 0'}),  # Spacer
                    correlation_description,
                    html.P(style={'margin': '10px 0'}),  # Spacer
                    volatility_description,
                    html.P(style={'margin': '10px 0'}),  # Spacer
                    #sharpe_description
                ], width=12),

                ], style={'padding': '20px'})
            ], 

                
            className="mb-4 shadow-sm"),
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading(dcc.Graph(id='price-graph', className='my-graph', config={'displayModeBar': False})),
                ], style={'padding': '20px'})
            ], className="mb-4 shadow-sm"),
        ], width=8),
    ], className="mb-4"),

    # Returns graph and Correlation graph side by side
    dbc.Row([
        # Returns graph
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading(dcc.Graph(id='returns-graph', className='my-graph')),
                ])
            ], style={'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px'}),
        ], width=6),  # Adjusted width to 6 for half the row

        # Correlation graph
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading(dcc.Graph(id='correlation-graph', className='my-graph')),
                ])
            ], style={'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px'}),
        ], width=6),  # Adjusted width to 6 for half the row
    ], className="mb-4"),


    # Volatility graph and Histogram for Distribution of Returns side by side
    dbc.Row([
        # Volatility graph
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading(dcc.Graph(id='volatility-graph', className='my-graph')),
                ])
            ], style={'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px'}),
        ], width=6),  # Adjusted width to 6 for half the row

        # Histogram for Distribution of Returns
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading(dcc.Graph(id='returns-distribution', className='my-graph')),
                ], style={'padding': '20px'})
            ], className="mb-4 shadow-sm"),
        ], width=6),  # Adjusted width to 6 for half the row
    ], className="mb-4"),


], fluid=True, 
style={
    'backgroundImage': 'linear-gradient(120deg, #f3f4f6, #f3f4f6)',
    'padding': '30px',
    'borderRadius': '15px',
    'boxShadow': '0px 0px 15px rgba(0, 0, 0, 0.05)'
})
