# %%
import pandas as pd
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
ticker_US = 'SPY'
ticker_HK = '2800.HK'
start_date = '2015-01-01'
end_date = '2019-12-31'
frequency = 'daily'
weight_US = 0.8
weight_HK = 0.2

# %%
df_US = get_price_table(ticker_US, start_date, end_date, frequency)
df_HK = get_price_table(ticker_HK, start_date, end_date, frequency)

# %%
df_portfolio = (pd.merge(df_US, df_HK, how='outer', left_index=True,
                         right_index=True, suffixes=('_US', '_HK'))
                [['adjclose_US', 'adjclose_HK']].fillna(method='ffill'))

# %%
df_portfolio[['US_return', 'HK_return']] = df_portfolio.pct_change()

# %%
df_portfolio['total_return'] = weight_US * \
    df_portfolio['US_return']+weight_HK*df_portfolio['HK_return']
