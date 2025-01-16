import tkinter as tk
from tkinter import ttk
import requests
# requests need to be installed
import time
import pandas as pd
# pandas need to be isntalled


# Function to fetch crypto price
def get_crypto_price(crypto_id, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[crypto_id][currency]
    except requests.exceptions.RequestException as e:
        return None

# Function to fetch and display the price
def fetch_price():
    crypto_id = crypto_var.get()
    currency = currency_var.get()
    price = get_crypto_price(crypto_id, currency)
    if price is not None:
        price_label.config(text=f"The price of {crypto_id} in {currency.upper()} is: {price}")
        save_price_to_csv(crypto_id, currency, price)
    else:
        price_label.config(text="Error fetching price!")

# Save price to a CSV file
def save_price_to_csv(crypto_id, currency, price, filename="crypto_prices.csv"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"Timestamp": [timestamp], "Crypto": [crypto_id], "Currency": [currency], "Price": [price]}
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

# Function to auto-fetch price
def auto_fetch():
    fetch_price()  # Fetch the price
    root.after(interval_ms, auto_fetch)  # Schedule the next fetch

# Tkinter GUI
root = tk.Tk()
root.title("Crypto Price Tracker")
root.geometry("400x200")

# Dropdown for selecting cryptocurrency
crypto_var = tk.StringVar(value="bitcoin")
crypto_dropdown = ttk.Combobox(root, textvariable=crypto_var, values=["bitcoin", "ethereum", "dogecoin", "cardano", "solana"])
crypto_dropdown.pack(pady=10)

# Dropdown for selecting currency
currency_var = tk.StringVar(value="usd")
currency_dropdown = ttk.Combobox(root, textvariable=currency_var, values=["usd", "eur", "gbp", "inr"])
currency_dropdown.pack(pady=10)

# Button to fetch price
fetch_button = ttk.Button(root, text="Fetch Price", command=fetch_price)
fetch_button.pack(pady=10)

# Label to display the price
price_label = ttk.Label(root, text="Select a cryptocurrency and currency to get the price.", font=("Arial", 12))
price_label.pack(pady=10)

# Auto-fetch interval in milliseconds (e.g., 60000ms = 60 seconds)
interval_ms = 30000  # 30 seconds

# Start auto-fetching
auto_fetch()

# Run the Tkinter main loop
root.mainloop()
