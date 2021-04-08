#https://github.com/TaylorFacen/nomics-python/wiki/Currencies#get-sparkline

# cd into Documents/Environments
# source crypto_env/bin/activate

from nomics import Nomics
import pandas as pd
import numpy as np

api_key = '1be400cebde55adc62e1fddc88618feb'

nomics = Nomics(api_key)

#markets = nomics.Markets.get_markets(exchange = 'binance')

#print(markets)

# ex_rate = nomics.ExchangeRates.get_history(
#     currency = "ADA",
#     start = "2021-03-01T00:00:00Z",
#     end = "2021-04-02T00:00:00Z"
# )

#print(ex_rate)
#curr = nomics.Currencies.get_currencies(ids = "VTX")

sp = nomics.Currencies.get_sparkline(
    start = "2019-01-01T00:00:00Z"
)

df = pd.DataFrame(sp)

def explode(df, lst_cols, fill_value=''):
    # make sure `lst_cols` is a list
    if lst_cols and not isinstance(lst_cols, list):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)

    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()

    if (lens > 0).all():
        # ALL lists in cells aren't empty
        return pd.DataFrame({
            col:np.repeat(df[col].values, df[lst_cols[0]].str.len())
            for col in idx_cols
        }).assign(**{col:np.concatenate(df[col].values) for col in lst_cols}) \
          .loc[:, df.columns]
    else:
        # at least one list in cells is empty
        return pd.DataFrame({
            col:np.repeat(df[col].values, df[lst_cols[0]].str.len())
            for col in idx_cols
        }).assign(**{col:np.concatenate(df[col].values) for col in lst_cols}) \
          .append(df.loc[lens==0, idx_cols]).fillna(fill_value) \
          .loc[:, df.columns]


lst_cols = ['timestamps', 'prices']

dfx = explode(df, lst_cols = lst_cols)

dfx.to_csv(r'//Users/alanjackson/Documents/Environments/crypto_env/Historical_Crypto_Prices_NomicsAPI.csv')



