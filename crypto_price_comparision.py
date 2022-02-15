import questionary
import fire
import os
import sys

"""
Program Description:
    This program will ask the user which of the available exchanges and trading pairs that the user 
    wants to compare the price of and in which exchange it is available at. Majority of the pricing
    data will be pulled from CoinGecko (https://www.coingecko.com/). The main focus of the program
    is as follows:
        - Allow the user to select a few cryptocurrency exchanges to compare to one another.
        - Allow the user to select a crpytocurrency of interest.
        - Display the current and historical prices of the specified crypto within the desired timerange
          and display it in an OHLC (possibly interactive) chart.
        - Provide a Monte Carlo simulation to see the potential risk-return in the short and long term.

Authors:
    
"""


def main():
    """
    Description:
        The main entry point into the program. All of the user input will be handled in this function.
    """

    pass


if __name__ == "__main__":
    fire.Fire(main)