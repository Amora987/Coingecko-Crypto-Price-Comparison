import questionary
import fire
import hvplot
import os
import sys

"""
Program Description:
    This program will ask the user which of the available exchanges and trading pairs that the user 
    wants to compare the price of and in which exchange it is available at. Majority of the pricing
    data will be pulled from CoinGecko (https://www.coingecko.com/). The main focus of the program
    is as follows:
        - Allow the user to select a crpytocurrency of interest (to keep it simple, the only coins available
          will be the ones that can be bought with USD).
        - Compare the price of the user select crypto to the list of supported exchanges.
        - Display the current and historical prices of the specified crypto within the desired timerange
          and display it in an OHLC (possibly interactive) chart.
        - Provide a Monte Carlo simulation to see the potential risk-return in the short and long term.

    Github Link: https://github.com/Amora987/Project-1 
"""


def main():
    """
    Description:
        The main entry point into the program. All of the user input will be handled in this function.
    """

    print("Welcome to the Crypto Price Comparison!")
    print("We currently support pricing for the following exchanges:")
    print("\tGemini\n\tCoinbase\n\tKraken\n\tFTX")
    
    # get the user to choose a coin
    availabe_coins = [ "Ethereum", "Bitcoin", "Dogecoin", "Polygon" ]
    choice = questionary.select(message = "Chose one of the following coins to continue:", choices = availabe_coins).ask()

    # pass the select coin and get the dataframe of exchange data obtained from the CoinGekco API
    choice = choice.lower().replace("polygon", "matic-network")
    

    # display the price charts from multiple exchanges for the selected coin 


    # perform a short-term Monte Carlo simulation and display the results


    # perform a long-term Monte Carlo simulation and display the results



if __name__ == "__main__":
    fire.Fire(main)