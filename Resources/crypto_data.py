import requests
import pandas as pd


DAILY_MARKET_CHARTS = "https://api.coingecko.com/api/v3/coins/{0}/market_chart?vs_currency=usd&days={1}&interval=daily"
