import questionary
import fire
import pandas as pd
import matplotlib.pyplot as plt
from Resources import crypto_data, Monte_Carlo_sim

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
    print("Select a crypto and we'll compare its price against various exchanges!")
    print("Currently, we only support crypto to USD pairs.")
    print("We currently support pricing for the following exchanges:")

    supported_exchanges = crypto_data.get_supported_exchange_names()
    for exchange in supported_exchanges:
        print(f"   - {exchange}")
    
    print() # just to print out a newline
    supported_coins = crypto_data.get_supported_crpyto_names() # get the coins that the user can choose
    choice = questionary.select(message = "Chose one of the following coins to continue:", choices = supported_coins).ask()

    # pass the select coin and get the dataframe of exchange data obtained from the CoinGekco API
    closing_prices_df = crypto_data.get_closing_price(choice)
    historical_prices_df = crypto_data.get_historical_data(choice)
    historical_prices_df.set_index(keys = "Timestamp", inplace = True)

    # bitcoin will be the benchmark to compare the other coin
    bitcoin_prices_df = crypto_data.get_historical_data("bitcoin")
    bitcoin_prices_df.set_index(keys = "Timestamp", inplace = True)

    # merge historical data with bitcoin data
    historical_prices_df = pd.concat([historical_prices_df, bitcoin_prices_df], axis = 1).dropna()
    historical_prices_df.columns = pd.MultiIndex.from_tuples([(choice, "Last"), ("Bitcoin", "Last")])

    print("\nCurrent Prices:")
    print(closing_prices_df)


    # setup the plot the current closing price for each supported exchange
    last_price = closing_prices_df["Last"]
    minimum = last_price.min() - (last_price.min() * 0.0025)
    maximum = last_price.max() + (last_price.max() * 0.0025)

    closing_prices_df.plot(
        kind = "bar",
        figsize = (15, 10),
        x = "Market",
        xlabel = "Exchange",
        y = "Last",
        ylabel = "Closing Prices",
        ylim = (minimum, maximum),
        title = f"Current Closing Price For {choice}"
    ).set_xticklabels(closing_prices_df["Market"], rotation = 0) # rotate the x-axis labels so it is horizontal


    # setup the plot to display the price charts from multiple exchanges for the selected coin 
    historical_prices_df.plot(
        kind = "line",
        figsize = (20, 10),
        xlabel = "Date",
        y = (choice, "Last"),
        ylabel = "Closing Prices",
        title = f"Daily Closing Price For {choice}"
    )


    # display the plots
    plt.show()


    # perform a Monte Carlo simulation and display the results
    mc = Monte_Carlo_sim.MonteCarloSim(historical_prices_df, [0.6, 0.4])

    print("\nHistorical Data")
    print(mc.portfolio_data)
    print(mc.calc_cumulative_return())

    # plot Monte Carlo simulation


if __name__ == "__main__":
    fire.Fire(main)