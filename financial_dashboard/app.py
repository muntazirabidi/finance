# app.py

from config import app
from layout import layout
import callbacks  # This will automatically execute the callbacks when imported

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True, port=8059)
