# Dash Financial Dashboard

Welcome to the Dash Financial Dashboard, a comprehensive and interactive tool I've developed using Plotly Dash in Python. This dashboard provides a deep dive into financial data, allowing users to visualize and analyze stock prices, index funds, and more, all in real-time.

## 🌟 Features

- **Multiple Stock/Fund Selection**: Choose and compare multiple stocks or funds simultaneously.
- **Time-Frame Flexibility**: Analyze data over various time frames - 1D, 5D, 1M, 1Y, 5Y, 10Y.
- **Investment Growth Visualization**: Witness the growth of an initial investment over the selected time frame.
- **Correlation Plots**: Understand how different stocks or funds correlate with each other.
- **Returns & Volatility**: Dive into the returns and volatility of your selected stocks/funds. Choose from various rolling windows to adjust volatility calculations.
- **Interactive & Responsive**: Every chart and graph is interactive, providing detailed insights upon hovering, zooming, or panning.

## 🛠️ Technologies Used

- **Framework**: Plotly Dash in Python
- **Data Source**: Yahoo Finance API (utilized via `yfinance` Python package)

## 🚀 Getting Started

### Prerequisites

Ensure you have Python and Pip installed.

### Installation

1. **Clone the Repository**:
`git clone https://github.com/muntazirabidi/finance/financial_dashboard.git`


2. **Install Dependencies**:
`pip install -r requirements.txt`


3. **Run the Application**:
`python app.py`


## 📁 Project Structure

- `app.py`: The main application file where the Dash app is initialized.
- `layout.py`: Contains the layout of the dashboard - all the UI components.
- `callbacks.py`: Houses the logic and interactivity of the dashboard.
- `utils.py`: Utility functions and helpers to assist with data fetching and processing.

## 🤝 Contribution

Your contributions are always welcome! If you have improvements or features you'd like to see, please open an issue or submit a pull request.

## 📜 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- **Yahoo Finance API**: For providing a wealth of financial data.
- **Plotly Dash Community**: For continuous support and resources.
