# Import libraries and dependencies
import os
import json
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import datetime as dt
import pytz


class MonteCarloSim:
    """
    A Python class for running a MonteCarlo simulation on portfolio of user.

    """

    def __init__(self, portfolio_data, weights="", num_simulations=1000, num_trade_days=252):

        # Check to make sure that all attributes are set.
        if not isinstance(portfolio_data, pd.DataFrame):
            raise TypeError("User data must be a DataFrame.")

        # Set weights if empty, otherwise make sure sum of weights equals one.
        if weights == "":
            num_crypto = len(
                portfolio_data.columns.get_level_values(0).unique())
            weights = [1.0/num_crypto for s in range(0, num_crypto)]
        else:
            if round(sum(weights), 2) < .99:
                raise AttributeError("Sum of portfolio weights must equal 1.")
# Maybe bug here
        # Calculate daily return if not within dataframe
        if not 'daily_return' in portfolio_data.columns.get_level_values(1).unique():
            close_df = portfolio_data.xs('last', level=1, axis=1).pct_change()
            tickers = portfolio_data.columns.get_level_values(0).unique()
            column_names = [(x, 'daily_return') for x in tickers]
            close_df.columns = pd.MultiIndex.from_tuples(column_names)
            portfolio_data = portfolio_data.merge(
                close_df, left_index=True).reindex(columns=tickers, level=0)

        # Select class attributes
        self.portfolio_data = portfolio_data
        self.weights = weights
        self.nSim = num_simulations
        self.nTrading = num_trade_days
        self.simulated_return = ""
# Maybe bug here

    def calc_cumulative_return(self):
        """
        Calculate the cumulative return of the crypto over time using the MonteCarlo simulation

        """
        # Get the crypto prices of each crypto
        last = self.portfolio_data.xs(
            'last', level=1, axis=1)[-1:].values.tolist()[0]

        # Calculate the mean and standard deviation of daily returns for each crypto
        daily_return = self.portfolio_data.xs('daily_return', level=1, axis=1)
        mean_return = daily_return.mean().tolist()
        std_return = daily_return.std().tolist()

        # Initialize empty DataFrame to hold the simulated prices
        portfolio_cumulative_returns = pd.DataFrame()

        # Run the simulation of projecting each crypto prices 'nSim' number of times
        for n in range(self.nSim):

            if n % 10 == 0:
                print(f"Running Monte Carlo simulation number of {n} times.")

            # Create a list of lists to contain the simulated values for each stock
            simvals = [[p] for p in last]

            # For each crypto in our data:
            for s in range(len(last)):

                # Simulate the returns for each trading day.
                for i in range(self.nTrading):

                    # Calculate the simulated values using the last price within the list
                    simvals[s].append(
                        simvals[s][-1] * (1 + np.random.normal(mean_return[s], std_return[s])))

                    # Calculate the daily returns of simulated prices
                    sim_df = pd.DataFrame(simvals).T.pct_change()

                    # Use the `dot` function with the weights to multiply weights with each columns simulated daily returns
                    sim_df = sim_df.dot(self.weights)

                    # Calculate the normalized, cumulative return series
                    portfolio_cumulative_returns[n] = (
                        1 + sim_df.fillna(0)).cumprod()

                # Set attribute to use in plotting
                self.simulated_return = portfolio_cumulative_returns

                # Calculate 95% confidence intervals for the final cumulative returns
                self.confidence_intervals = portfolio_cumulative_returns.iloc[-1, :].quantile(
                    q-[.025, .975])

                return portfolio_cumulative_returns

    def plot_simulation(self):
        """
        Visualizes the simulated stock trajectories using calc_cumulative_return method.
        """
        # Check to make sure that simulation has run previously.
        if not isinstance(self.simulated_return, pd.DataFrame):
            self.calc_cumulative_return()

        # Use Pandas plot function to plot the return data
        plot_title = f"{self.nSim} Simulations of Cumulative Portfolio Return Trajectories Over the Next {self.nTrading} Trading Days."

        return self.simulated_return.plot(legend=None, title=plot_title)

    def plot_distribution(self):
        """
        Visualize the distribution of cumulative returns simulated using calc_cumulative_return method.
        """

        # Check to make sure that the simulation has run previously.
        if not isinstance(self.simulated_return, pd.DataFrame):
            self.calc_cumulative_return()

        # Use the `plot` function to create a probability distribution histogram of simulated ending values with markings for a 95% confidence interval
        plot_title = f"Distribution of Final Cumulative Returns Across All {self.nSim} Simulations."
        plt = self.simulated_return.iloc[-1, :].plot(
            kind='hist', bins=10, density=True, title=plot_title)
        plt.axvline(self.confidence_intervals.iloc[0], color='r')
        plt.axvline(self.confidence_intervals.iloc[1], color='r')

        return plt

    def summarize_cumulative_return(self):
        """
        Calculate final summary statistics for Monte Carlo simulated stock data.
        """

        # Check to make sure that simulation has run previously
        if not isinstance(self.simulated_return, pd.DataFrame):
            self.calc_cumulative_return()

        metrics = self.simulated_return.iloc[-1].describe()
        ci_series = self.confidence_intervals
        ci_series.index = ['95% CI Lower', '95% CI Upper']

        return metrics.append(ci_series)
