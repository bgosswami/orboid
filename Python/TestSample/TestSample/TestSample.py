import os
import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir="../../Data/"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        # TODO: Read and join data for each symbol
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col="Date", 
                        parse_dates=True, usecols=['Date', 'Adj Close'],
                        na_values=['Nan'])
        df_temp = df_temp.rename(columns={'Adj Close':symbol})
        df = df.join(df_temp, how='inner', sort=True)
    return df

def normalize_data(df):
    return df/df.ix[0,:]

def plot_data(df, title="Stock prices"):
    ax= df.plot(title=title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    plot_data(df.ix[start_index:end_index, columns])    

def test_run():
    # Define a date range
    dates = pd.date_range('2017-01-01', '2018-01-08')

    # Choose stock symbols to read
    symbols = ['AAPL', 'IBM', 'SPY']
    
    # Get stock data
    df = get_data(symbols, dates)

    # slicing data frames
    sDate = '2017-12-04'
    eDate = '2017-12-08'
    
    # Row slicing
    dfRow = df.ix[sDate:eDate]

    #col slicing
    dfCol = dfRow[['AAPL', 'SPY']]
    
    #slicing in both dimension
    dfBoth = df.ix[sDate:eDate, ['AAPL', 'IBM']]

#    plot_selected(df, ['AAPL', 'IBM'], sDate, eDate)
    plot_data(normalize_data(df))


if __name__ == "__main__":
    test_run()
