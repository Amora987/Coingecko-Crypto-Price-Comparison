import requests
import pandas as pd
from sympy import E


# The api for getting daily closing prices
DAILY_MARKET_CHARTS = "https://api.coingecko.com/api/v3/coins/{0}/market_chart?vs_currency=usd&days={1}&interval=daily"

# The api for tickers that the user will decide from
CRYPTO_URL = "https://api.coingecko.com/api/v3/exchanges/{0}/tickers?coin_ids={1}"


# list of markets places user can purchase crypto and cryptos available
supported_exchanges = {
    "Gemini" : "gemini", 
    "Coinbase" : "gdax", 
    "Kraken" : "kraken", 
    "FTX" : "ftx_spot"
}

# a dictionary of supported cryptos
supported_crpytos = { 
    "Bitcoin" : "bitcoin", 
    "Ethereum" : "ethereum", 
    "Dogecoin" : "dogecoin", 
    "Polygon" : "matic-network" 
}


def get_supported_exchange_names():
    return supported_exchanges.keys()


def get_supported_exchange_id(exchange):
    return supported_exchanges[exchange]


def get_supported_crpyto_names():
    return supported_crpytos.keys()


def get_supported_crypto_id(crypto):
    return supported_crpytos[crypto]


def get_closing_price(crypto):
    """
    Description:
        Grabs the current closing price of the specified crypto for each exchange.
    """

    coin_id = get_supported_crypto_id(crypto)
    dataframe = pd.DataFrame(columns = ["Timestamp", "Market", "Base", "Last"])

    for exchange in supported_exchanges.values():
        platform = requests.get(CRYPTO_URL.format(exchange, coin_id)).json()
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

    coin_id = get_supported_crypto_id(crypto)
    daily_data = requests.get(DAILY_MARKET_CHARTS.format(coin_id, days)).json()
    
    timestamp = []
    prices = []
    for data in daily_data["prices"]:
        timestamp.append(pd.Timestamp(data[0], tz = "America/Chicago", unit = "ms"))
        prices.append(data[1])

    return pd.DataFrame(data = { "Timestamp" : timestamp, "Prices" : prices })

