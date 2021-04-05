from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd


api_key = '231f04b7-44ce-4dcd-8dfd-0f0e0e1fbda4'


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1'
  , 'limit':'5000'
  , 'convert':'USD'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  json_text = json.loads(response.text)
  data = json_text['data']

  df = pd.json_normalize(data)

  df_short = df[['symbol', 'slug', 'date_added', 'last_updated', 'quote.USD.price', 'quote.USD.volume_24h', 'quote.USD.market_cap', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']]
  
  crypto_tickers = ['CVC', 'LSK', 'OMG', 'BTC', 'ETH', 'NEO', 'ADA', 'OCEAN', 'DOT', 'TRAC', 'MRPH', 'BAL', 'ZRX'
                    'COMP', 'MKR', 'SNX', 'BNB', 'LINK', 'UNI', 'XMR', 'ALGO', 'UMA', 'REN', 'BAT', 'ONT'
                    , 'KNC', 'UBT', 'OMI', 'EWT', 'SOL', 'WPR', 'XLM', 'ATOM', 'XRP', 'EOS', 'MANA', 'STORJ', 'SC'
                    , 'VTX', 'DWZ', 'CAKE', 'PNT', 'CHART', 'BLANK', 'TRB', 'DVG', 'ALPA', 'PHA', 'KSM', 'BLES']

  #df_short.crypto_tickers.isin(crypto_tickers)
  df_out = df_short[df_short['symbol'].isin(crypto_tickers)]
#  df_out.to_csv(r'coinmarketcap_api_v2.csv')
  df_out.columns = ['symbol', 'name', 'date_added', 'last_updated', 'price_usd', 'volume_24h', 'market_cap', 'percent_change_24h', 'percent_change_7d', 'percent_change_30d', 'percent_change_60d', 'percent_change_90d']

  win_path = r'C:\\Users\\aljackson\\Documents\\Environments\\crypto_api\\CoinmarketcapAPI_Crypto_Data.csv'
  df_out.to_csv(win_path, mode = 'a', index = False, header = False)

  # for x in data:
  # 	crypto_list.append(x['symbol'], x['slug'], x['date_added'], x['last_updated'], x['quote']['USD']['price'])
#  	print(x['symbol'], x['slug'], x['date_added'], x['last_updated'], x['quote']['USD']['price'])

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print('except error: check code')


