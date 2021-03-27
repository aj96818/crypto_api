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
  
  df_short.to_csv(r'coinmarketcap_api.csv')




  





  # for x in data:
  # 	crypto_list.append(x['symbol'], x['slug'], x['date_added'], x['last_updated'], x['quote']['USD']['price'])
 


#  	print(x['symbol'], x['slug'], x['date_added'], x['last_updated'], x['quote']['USD']['price'])

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print('except error: check code')


