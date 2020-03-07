import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data, wb

if __name__ == '__main__':
    # collect time series for S&P 500
    sp500 = data.DataReader('^GSPC', data_source='yahoo', start='1/1/2000')
    
    # estimate two-month and one-year trends
    sp500['42d'] = np.round(sp500['Close'].rolling(window=42).mean(), 2)
    sp500['252d'] = np.round(sp500['Close'].rolling(window=252).mean(), 2)

    # trading singals
    sp500['42-252'] = sp500['42d'] - sp500['252d']
    SD = 50 # signal threshold
    sp500['Regime'] = np.where(sp500['42-252'] > SD, 1, 0)
    sp500['Regime'] = np.where(sp500['42-252'] < -SD, -1, sp500['Regime'])
    sp500['Market'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
    sp500['Strategy'] = sp500['Regime'].shift(1) * sp500['Market']

    # plot trends over close quotes; strategy vs. market
    sp500[['Close', '42d', '252d']].plot(grid=True, figsize=(8,6))
    sp500[['Market', 'Strategy']].cumsum().apply(np.exp).plot(grid=True, figsize=(8,6))
    plt.show(block=True)

