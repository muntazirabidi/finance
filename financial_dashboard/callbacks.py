from config import app, yf, pd, go, Input, Output
from datetime import datetime, timedelta
import plotly.express as px
from layout import fetch_fund_info

# Define font_dict here
font_dict = {
    'family': "'Helvetica Neue', Arial, sans-serif",
    'size': 14
}


colors = {
    'background': '#F4F4F4',  # Light gray
    'text': '#2C3E50'  # Deep navy
}



@app.callback(
    [Output('price-graph', 'figure'),
     Output('returns-graph', 'figure'),
     Output('correlation-graph', 'figure'),
     Output('volatility-graph', 'figure'),  # <-- Add this line
     Output('returns-distribution', 'figure')],  # <-- Add this line
    [Input('fund-dropdown', 'value'),
     Input('time-frame-dropdown', 'value'),
     Input('volatility-window-dropdown', 'value')]
)

def update_graphs(selected_funds, time_frame,volatility_window):
    end_date = datetime.today().strftime('%Y-%m-%d')

    # Define start date based on the selected time frame
    if time_frame == '1Y':
        start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    elif time_frame == '5D':
        start_date = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')
    elif time_frame == '1D':
        start_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    elif time_frame == '1M':
        start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    elif time_frame == '3Y':
        start_date = (datetime.today() - timedelta(days=3*365)).strftime('%Y-%m-%d')
    elif time_frame == '5Y':
        start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    elif time_frame == '10Y':
        start_date = (datetime.today() - timedelta(days=10*365)).strftime('%Y-%m-%d')
    else:
        start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

    ticker_map = {
        'S&P500 VOO': 'VOO',
        'S&P500 VUSA': 'VUSA.L',
        'US STOCK MARKET': 'VTI',
        'RUSSELL_2000': 'IWM',
        'SMALL_CAP': 'VB',
        'MID_CAP': 'VO',
        'NASDAQ100': 'QQQ',
        'Vertex Pharma': 'VRTX',
        'FTSE All-World ETF': 'VWRL.L',
        'FTSE All-World High Dividend': 'VHYL.L',
        'FTSE 100 ETF': 'VUKE.L',
        'Bitcoin GBP': 'BTC-GBP',
        'ETH GBP': 'ETH-GBP',

        # Additional Vanguard funds
        'TOTAL BOND MARKET': 'BND',
        'INTERNATIONAL STOCK INDEX': 'VXUS',
        'EMERGING MARKETS STOCK INDEX': 'VWO',
        'TOTAL WORLD STOCK ETF': 'VT',
        'REAL ESTATE ETF': 'VNQ',
        'TOTAL CORPORATE BOND ETF': 'VTC',

        # Additional iShares funds
        'MSCI Emerging Markets': 'EEM',
        'MSCI EAFE': 'EFA',
        'Core U.S. Aggregate Bond': 'AGG',
        'iBoxx $ Investment Grade Corporate Bond': 'LQD',
        'U.S. Real Estate': 'IYR',
        'Russell 1000 Growth': 'IWF',

         # iShares S&P 500 funds in GBP
        'iShares S&P 500 GBP Dist': 'VUSD.L',
        'iShares S&P 500 (Hedged/GBP/Dist)': 'GSPX',
        'iShares S&P 500 (USD/Accm)': 'IUSA.L'
    
    } 

    dfs = {}
    for fund in selected_funds:
        ticker = ticker_map[fund]
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            dfs[fund] = data['Close']
        except Exception as e:
            print(f"Error fetching data for {fund}: {e}")
            dfs[fund] = pd.Series()

    df = pd.concat(dfs, axis=1)

    # Forward-fill the missing values
    df.fillna(method='ffill', inplace=True)

    if all(df[fund].empty for fund in selected_funds):
        return {
            'data': [],
            'layout': {
                'title': 'Error fetching data for selected funds. Please try again later.',
                'font': font_dict
            }
        }

    # For Investment Growth
    df_investment = df.copy()
    for fund in selected_funds:
        df_investment[fund] = (df[fund] / df[fund].iloc[0]) * 1000
    investment_data = [go.Scatter(x=df_investment.index, y=df_investment[fund], mode='lines', name=fund) for fund in selected_funds]

    investment_figure = px.line(df_investment, x=df_investment.index, y=selected_funds, 
                            title='Investment Growth of GBP 1000 Over Time',
                            template='plotly_white')  # Using a clean template

    investment_figure.update_layout(
        font=font_dict,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title={
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(l=40, r=20, t=40, b=40),
        hovermode='x unified',
        xaxis_title="Date",
        yaxis_title="Investment Growth",
        legend_title="Funds",
        xaxis={
            'gridcolor': '#d1d1d1',  # A lighter gray color for the x-axis grid
            'gridwidth': 1.5  # Slightly increased grid line width
        },
        yaxis={
            'gridcolor': '#d1d1d1',  # A lighter gray color for the y-axis grid
            'gridwidth': 1.5  # Slightly increased grid line width
        }
    )



    # For Returns in Percentage
    if time_frame == '1Y':
        df_resampled = df.resample('M').last()
    elif time_frame in ['3Y', '5Y', '10Y']:
        df_resampled = df.resample('A').last()
    else:
        df_resampled = df
    df_returns = df_resampled[selected_funds].pct_change().dropna() * 100
    returns_figure = px.bar(df_returns, x=df_returns.index, y=selected_funds, title='Returns in Percentage Over Time')
    returns_figure.update_layout(font=font_dict, plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'], barmode='group')


    # For Correlation Matrix
    correlation_matrix = df[selected_funds].corr()

    # Create the heatmap with enhanced aesthetics
    correlation_figure = px.imshow(
    correlation_matrix,
    color_continuous_scale='RdBu_r',  # Light color scale
    title='Fund Correlation Matrix',
    labels=dict(color="Correlation Coefficient")
    )


    # Update layout for a professional look
    correlation_figure.update_layout(
        font=font_dict,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        margin=dict(t=100, l=0, r=0, b=0),  # Adjust margins for a tighter fit
        xaxis_title="Funds",
        yaxis_title="Funds",
        coloraxis_colorbar=dict(
            title="Correlation Coefficient",
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["-1", "-0.5", "0", "0.5", "1"]
        )
    )

    # Add annotations to display the correlation values
    for i, row in enumerate(correlation_matrix.values):
        for j, value in enumerate(row):
            correlation_figure.add_annotation(
                dict(
                    x=correlation_matrix.columns[j],
                    y=correlation_matrix.index[i],
                    text=round(value, 2),
                    showarrow=False,
                    font=dict(color='black' if -0.5 < value < 0.5 else 'white')
                )
            )



    window_size = int(volatility_window[:-1])  # Extract the number from the string (e.g., '5D' -> 5)
    rolling_volatility = df[selected_funds].rolling(window=window_size).std()


    # For Rolling Volatility
    volatility_figure = px.line(rolling_volatility, x=rolling_volatility.index, y=selected_funds, title='10-Day Rolling Volatility')
    volatility_figure.update_layout(font=font_dict, plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])

    


    # ... [Your existing callback code]

    # Compute daily returns for each fund
    df_returns = df[selected_funds].pct_change().dropna()



    # For Distribution of Returns
    def plot_return_distribution(fund_name):
        fig = px.histogram(df_returns, x=fund_name, nbins=100, title=f'Distribution of Returns')
        fig.update_layout(
            font=font_dict,
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            xaxis_title="Return",
            yaxis_title="Frequency",
            margin=dict(l=40, r=20, t=40, b=40)
        )
        return fig

    # If multiple funds are selected, we'll just show the distribution for the first fund for simplicity.
    # You can modify this as per your requirements.
    return_dist_figure = plot_return_distribution(selected_funds) if selected_funds else None


    # Update the return statement of your callback to include return_dist_figure
    return investment_figure, returns_figure, correlation_figure, volatility_figure, return_dist_figure