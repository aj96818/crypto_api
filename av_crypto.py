# Premium API Key: W1U7T09FFM4DY97N

import time
import pandas as pd
import alpha_vantage
import requests
import requests_html
import json

startTime = time.time()

crypto = ['LINK', 'BTC', 'ETH', 'ZRX', 'BAL', 'BAT', 'BCH', 'KNC', 'LSK', 'IOTA', 'MRPH', 'NEO', 'ONT', 'DOT', 'POWR', 'REN', 'XLM', 'UBT', 'WPR']

df_list = []
for ticker in crypto:
	try:
		API_URL = "https://www.alphavantage.co/query" 
		data = { 
			"function": 'CURRENCY_EXCHANGE_RATE', 
			"from_currency": ticker,
			"to_currency" : 'USD',
			"datatype": "json", 
			"apikey": 'W1U7T09FFM4DY97N'} 

		response = requests.get(API_URL, data) 
		response_json = response.json() # may be redundant
		
		x = json.dumps(response_json)
		d = json.loads(x)
		e = d['Realtime Currency Exchange Rate']
		a = dict((k, e[k]) for k in ('1. From_Currency Code', '2. From_Currency Name', '3. To_Currency Code', '4. To_Currency Name', '5. Exchange Rate', '6. Last Refreshed', '7. Time Zone', '8. Bid Price', '9. Ask Price'))	

		df = pd.DataFrame.from_dict(a, orient = 'index')
		df = df.transpose()
		df = df.drop(['4. To_Currency Name'], axis=1)
		df_list.append(df)
		time.sleep(2)
	except:
		pass

newdata_df = pd.concat(df_list, ignore_index = True)

df_out = newdata_df

mac_path = r'//Users/alanjackson/Documents/Environments/stocks_env/AV_Crypto_Data.csv'
win_path = r'C:\\Users\\aljackson\\Documents\\Environments\\py_yfinance\\AV_Crypto_Data.csv'

df_out.to_csv(win_path, mode = 'a', index = False, header = False)

executionTime = (time.time() - startTime)
print('Execution time in minutes: ' + str(executionTime/60))
