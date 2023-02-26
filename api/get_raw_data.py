import sqlite3

import pandas as pd
import requests

# Define API key and endpoint
API_KEY = "YOUR_API_KEY_HERE"
ENDPOINT = "https://www.alphavantage.co/query"

# Define stock symbols to retrieve data for
SYMBOLS = ["IBM", "AAPL"]

# Define database connection and cursor
conn = sqlite3.connect("financial_stock.db")
c = conn.cursor()

# Create financial_data table if it doesn't exist
c.execute("""CREATE TABLE IF NOT EXISTS financial_data (
                symbol TEXT,
                date TEXT,
                open_price FLOAT,
                close_price FLOAT,
                volume FLOAT,
                page INTEGER,
                PRIMARY KEY (symbol, date, page)
             );""")

# Retrieve data for the most recent two weeks for each symbol
for symbol in SYMBOLS:
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(ENDPOINT, params=params)
    data = response.json()["Time Series (Daily)"]
    df = pd.DataFrame(data).transpose()
    df = df.iloc[:10]  # Retrieve only the most recent 10 days of data
    df = df.reset_index()
    df = df.rename(columns={
        "index": "date",
        "1. open": "open_price",
        "4. close": "close_price",
        "6. volume": "volume"
    })
    df["symbol"] = symbol
    df["page"] = 1

    # Insert data into financial_data table, ignoring duplicates
    for i, row in df.iterrows():
        c.execute("""INSERT OR IGNORE INTO financial_data
                        (symbol, date, open_price, close_price, volume, page)
                        VALUES (?, ?, ?, ?, ?, ?);""",
                  (row["symbol"], row["date"], row["open_price"], row["close_price"], row["volume"], row["page"]))
    
# Commit changes and close connection
conn.commit()
conn.close()
