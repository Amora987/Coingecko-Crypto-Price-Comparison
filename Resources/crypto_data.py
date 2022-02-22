import requests
import pandas as pd


# The api for getting daily closing prices
DAILY_MARKET_CHARTS = "https://api.coingecko.com/api/v3/coins/{0}/market_chart?vs_currency=usd&days={1}&interval=daily"

# The api for tickers that the user will decide from
CRYPTO_URL = "https://api.coingecko.com/api/v3/exchanges/{0}/tickers?coin_ids={1}"


# list of markets places user can purchase crypto and cryptos available
top_five = ["gemini", "gdax", "kraken", "ftx_spot"]
crypto_list = ["ethereum", "bitcoin", "dogecoin", "matic-network"]


def get_closing_price(crypto):
    """
    Description:
        Grabs the current closing price of the specified crypto for each exchange.
    """

    dataframe = pd.DataFrame(columns = ["Timestamp", "Market", "Base", "Last"])
    for exchange in top_five:
        platform = requests.get(CRYPTO_URL.format(exchange, crypto)).json()
        for currency in platform["tickers"]:
            if currency["target"] == "USD":
                #print(json.dumps(currency,indent = 4, sort_keys = True))
                time = pd.Timestamp(currency["timestamp"], tz = "America/Chicago")
                # set the colmumns (keys from the dictionary) to match the of each coin and exchange values 
                dataframe.loc[len(dataframe.index)] = [time, currency["market"]["name"], currency["base"], currency["last"]]
    
    return dataframe


def get_historical_data(crypto, days = 30):
    """
    Description:
        Grabs the historical data for the specified amount of days.
    """

    daily_data = requests.get(DAILY_MARKET_CHARTS.format(crypto, days)).json()

    timestamp = []
    prices = []
    for data in daily_data["prices"]:
        timestamp.append(pd.Timestamp(data[0], tz = "America/Chicago", unit = "ms"))
        prices.append(data[1])

    return pd.DataFrame(data = { "Timestamp" : timestamp, "Prices" : prices })

