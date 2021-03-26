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
  data = json.loads(response.text)
  df = pd.DataFrame.from_dict(data, orient = 'index')
  print(df)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print('except error: check code')


		# x = json.dumps(response_json)
		# d = json.loads(x)
		# e = d['quarterlyEarnings'][:10]
		
		# for dic in e:
		# 	df = pd.DataFrame.from_dict(dic, orient = 'index')
		# 	df = df.transpose()
		# 	df['symbol'] = ticker
		# 	eps_list.append(df)
		# 	time.sleep(2)