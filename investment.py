# %%
import pandas as pd
import numpy as np
from yahoofinancials import YahooFinancials


# %%
def get_price_table(ticker, start_date, end_date, frequency):
    yahoo_financials = YahooFinancials(ticker)
    df = pd.DataFrame(yahoo_financials.get_historical_price_data(
        start_date, end_date, frequency)[ticker]['prices'])
    df['formatted_date'] = pd.to_datetime(df['formatted_date'])
    df.set_index('formatted_date', inplace=True)
    df.index.name = 'date'
    return df


# %%
def get_stats(ticker_US, ticker_HK, start_date, end_date, weight_US, stats='sharpe'):

    frequency = 'daily'
    weight_HK = 1-weight_US

    df_US = get_price_table(ticker_US, start_date, end_date, frequency)
    df_HK = get_price_table(ticker_HK, start_date, end_date, frequency)

    df = (pd.merge(df_US, df_HK, how='outer', left_index=True,
                   right_index=True, suffixes=('_US', '_HK'))
          [['adjclose_US', 'adjclose_HK']].fillna(method='ffill'))

    df['price_weighted'] = weight_US * \
        df['adjclose_US']+weight_HK*df['adjclose_HK']

    df[['log_price_US', 'log_price_HK', 'log_price_weighted']] = df[[
        'adjclose_US', 'adjclose_HK', 'price_weighted']].applymap(np.log)

    df[['log_return_US', 'log_return_HK', 'log_return_weighted']] = df[[
        'log_price_US', 'log_price_HK', 'log_price_weighted']].diff()

    mean_return = df[['log_return_US',
                      'log_return_HK', 'log_return_weighted']].mean()
    vol_return = df[['log_return_US',
                     'log_return_HK', 'log_return_weighted']].std()

    sharpe_ratio = mean_return/vol_return

    corr = df['log_return_US'].corr(df['log_return_HK'])

    stats_sharpe = pd.DataFrame({'return_mean': mean_return,
                                 'return_volatility': vol_return, 'sharpe_ratio': sharpe_ratio})
    if stats == 'sharpe':
        return stats_sharpe
    elif stats == 'correlation':
        return corr
    else:
        return 'invalid stats'


# %%
ticker_US = 'SPY'
ticker_HK = '2800.HK'
start_date = '2015-01-01'
end_date = '2019-12-31'
weight_US = 0.8

# %%
frequency = 'daily'
weight_HK = 1-weight_US

# %%
df_US = get_price_table(ticker_US, start_date, end_date, frequency)
df_HK = get_price_table(ticker_HK, start_date, end_date, frequency)

# %%
df = (pd.merge(df_US, df_HK, how='outer', left_index=True,
               right_index=True, suffixes=('_US', '_HK'))
      [['adjclose_US', 'adjclose_HK']].fillna(method='ffill'))

# %%
df['price_weighted'] = weight_US * \
    df['adjclose_US']+weight_HK*df['adjclose_HK']

# %%
df[['log_price_US', 'log_price_HK', 'log_price_weighted']] = df[[
    'adjclose_US', 'adjclose_HK', 'price_weighted']].applymap(np.log)

# %%
df[['log_return_US', 'log_return_HK', 'log_return_weighted']] = df[[
    'log_price_US', 'log_price_HK', 'log_price_weighted']].diff()

# %%
mean_return = df[['log_return_US',
                  'log_return_HK', 'log_return_weighted']].mean()
vol_return = df[['log_return_US',
                 'log_return_HK', 'log_return_weighted']].std()

# %%
sharpe_ratio = mean_return/vol_return

# %%
corr = df['log_return_US'].corr(df['log_return_HK'])

# %%
stats_sharpe = pd.DataFrame({'return_mean': mean_return,
                             'return_volatility': vol_return, 'sharpe_ratio': sharpe_ratio})

# %%
ticker_US = 'SPY'
ticker_HK = '2800.HK'
start_date = '2015-01-01'
end_date = '2019-12-31'

# %%
df_portfolio_compare = pd.DataFrame(
    columns=['US_weight', 'return_mean', 'return_volatility', 'sharpe_ratio'])

# %%
for weight_US in np.linspace(0, 1, 11):
    stats_portfolio = get_stats(ticker_US, ticker_HK, start_date,
                                end_date, weight_US, stats='sharpe').loc['log_return_weighted']
    series_portfolio = pd.Series({'US_weight': weight_US,
                                  'return_mean': stats_portfolio['return_mean'],
                                  'return_volatility': stats_portfolio['return_volatility'],
                                  'sharpe_ratio': stats_portfolio['sharpe_ratio']})
    df_portfolio_compare = df_portfolio_compare.append(
        series_portfolio, ignore_index=True)

# %%
