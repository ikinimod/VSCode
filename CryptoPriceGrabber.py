import tkinter as tk
from tkinter import ttk
import requests
# requests need to be installed
from datetime import datetime
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


# Function to fetch and display the price for the top section
def fetch_top_price():
    crypto_id = top_crypto_var.get()
    currency = top_currency_var.get()
    price = get_crypto_price(crypto_id, currency)
    if price is not None:
        top_price_label.config(text=f"Der Preis von {crypto_id} in {currency.upper()} ist: {price}")
        save_price_to_csv(crypto_id, currency, price)
    else:
        top_price_label.config(text="Fehler beim Abrufen des Preises!")


  # Function to auto-fetch prices for multiple cryptos
# def fetch_multiple_prices():
#     for crypto_id in multiple_cryptos:
#         price = get_crypto_price(crypto_id, "usd")
#         if price is not None:
#             multiple_prices_labels[crypto_id].config(text=f"{crypto_id.capitalize()}: {price} USD")
#         else:
#             multiple_prices_labels[crypto_id].config(text=f"{crypto_id.capitalize()}: Fehler beim Abrufen!")
#     root.after(auto_fetch_interval, fetch_multiple_prices)  # Schedule the next fetch


# Save price to a CSV file
def save_price_to_csv(crypto_id, currency, price, filename="C:/Users/domin/Documents/crypto_prices.csv"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"Timestamp": [timestamp], "Crypto": [crypto_id], "Currency": [currency], "Price": [price]}
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)


# Tkinter GUI
root = tk.Tk()
root.title("Crypto Price Tracker")
root.geometry("500x400")
root.configure(bg="#2E3B4E")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), background="#2E3B4E", foreground="white")

# Top section for manual fetching
top_crypto_var = tk.StringVar(value="bitcoin")
top_currency_var = tk.StringVar(value="usd")

ttk.Label(root, text="Kryptowährung auswählen:").pack(pady=5)
top_crypto_dropdown = ttk.Combobox(root, textvariable=top_crypto_var, values=["bitcoin", "ethereum", "dogecoin", "cardano", "solana", "ripple"])
top_crypto_dropdown.pack(pady=5)

ttk.Label(root, text="Währung auswählen:").pack(pady=5)
top_currency_dropdown = ttk.Combobox(root, textvariable=top_currency_var, values=["usd", "eur", "gbp", "inr"])
top_currency_dropdown.pack(pady=5)

fetch_button = ttk.Button(root, text="Preis aktualisieren", command=fetch_top_price)
fetch_button.pack(pady=10)

top_price_label = ttk.Label(root, text="Wähle eine Kryptowährung und eine Währung")
top_price_label.pack(pady=10)

  # Bottom section for auto-fetching multiple cryptos
# ttk.Label(root, text="Live-Preise für mehrere Kryptowährungen:").pack(pady=10)

# multiple_cryptos = ["bitcoin", "ethereum", "dogecoin"]
# multiple_prices_labels = {}

  # for crypto in multiple_cryptos:
#     label = ttk.Label(root, text=f"{crypto.capitalize()}: --")
#     label.pack()
#     multiple_prices_labels[crypto] = label

# Auto-fetch interval in milliseconds
auto_fetch_interval = 30000  # 30 seconds

# fetch_multiple_prices()  # Start auto-fetching

# Run the Tkinter main loop
root.mainloop()
