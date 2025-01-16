import requests
import time

def get_crypto_price(crypto_id, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[crypto_id][currency]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def track_price(crypto_id, currency, interval=60):
    while True:
        price = get_crypto_price(crypto_id, currency)
        if price is not None:
            print(f"The current price of {crypto_id} in {currency} is: {price} {currency.upper()}")
        time.sleep(interval)

if __name__ == "__main__":
    # Track Bitcoin price in USD every 30 seconds
    track_price("bitcoin", "usd", interval=30)
