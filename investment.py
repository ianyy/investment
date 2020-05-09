# %%
import pandas as pd
from yahoofinancials import YahooFinancials


# %%
ticker = 'AAPL'
yahoo_financials = YahooFinancials(ticker)


# %%
df = pd.DataFrame(yahoo_financials.get_historical_price_data(
    '2018-01-01', '2019-03-19', 'daily')[ticker]['prices'])


# %%
df.set_index('formatted_date', inplace=True)

# %%
df.head()
