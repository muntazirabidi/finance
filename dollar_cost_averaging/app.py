import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from data_utils import fetch_data, compute_dca
from layout import layout
import pandas as pd
import dash_html_components as html


app = dash.Dash(__name__)
app.layout = layout

def calculate_portfolio_growth(data, frequency, lumpsum):
    """Calculate the growth of the portfolio over time given a DCA strategy."""
    values = []
    num_periods = 1  # default for lumpsum

    if frequency == 'monthly':
        dates = pd.date_range(data.index[0], data.index[-1], freq='MS')
    elif frequency == 'weekly':
        dates = pd.date_range(data.index[0], data.index[-1], freq='W-MON')
    elif frequency == 'biweekly':
        dates = pd.date_range(data.index[0], data.index[-1], freq='2W-MON')
    elif frequency == 'lumpsum':
        dates = [data.index[0]]  # lumpsum will be invested on the first date
    else:
        raise ValueError("Invalid frequency")
    
    num_periods = len(dates)
    amount_per_period = lumpsum / num_periods

    shares_bought = 0

    for date in data.index:
        if date in dates:
            shares_bought += amount_per_period / data[date]
        values.append(shares_bought * data[date])

    return values

@app.callback(
    [Output('graph-strategy', 'figure'),
     Output('net-profit-display', 'children')],
    [Input('dropdown-stock', 'value'),
     Input('dropdown-frequency', 'value'),
     Input('date-picker-start', 'date'),
     Input('date-picker-end', 'date'),
     Input('input-lumpsum', 'value')]
)
def update_graph(selected_stock, selected_frequencies, start_date, end_date, lumpsum):
    data = fetch_data(ticker=selected_stock, start_date=start_date, end_date=end_date)
    # Define the fig using make_subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=("", ""))
    
    colors = {
        'monthly': '#3498db',
        'weekly': '#e74c3c',
        'biweekly': '#2ecc71',
        'lumpsum': '#f39c12'
    }
    
    profit_data = []
    annotations = []

    bar_names = ['Invested', 'Final Value', 'Profit']

    # Combine the plotting logic into one loop
    for frequency in selected_frequencies:
        amount = lumpsum

        
        portfolio_growth = calculate_portfolio_growth(data, frequency, amount)
        label = f'{frequency.capitalize()}' if frequency != 'lumpsum' else 'Lump Sum'
        
        fig.add_trace(go.Scatter(x=data.index, y=portfolio_growth, mode='lines', name=label, line=dict(color=colors[frequency])), row=1, col=1)
        
        final_value, invested = compute_dca(data, frequency, amount)
        profit = final_value - invested

        fig.add_trace(go.Bar(name=label, x=bar_names, y=[invested, final_value, profit], marker_color=colors[frequency]), row=1, col=2)
        
        profit_data.append((label, profit))

        

    fig.update_layout(
        title_font=dict(size=20),
        margin=dict(l=40, r=40, b=40, t=40, pad=5),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family='Arial'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        annotations=annotations
    )
    
    fig.update_yaxes(title_text='Portfolio Value (£)', col=1)
    fig.update_yaxes(title_text='Amount (£)', col=2)

    net_profit_display = html.Table(
        # Header
        [html.Tr([html.Th("Strategy"), html.Th("Net Profit (£)")])] +
        # Body
        [html.Tr([html.Td(strategy), html.Td(f"£{profit:.2f}")]) for strategy, profit in profit_data]
    )

    return fig, net_profit_display


if __name__ == '__main__':
    app.run_server(debug=True, port=8056)
