  
 #This example uses Python 2.7 and the python-request library.


'''
Steps for execution:
1) cd to Documents/Environments
2) activate crypto_api_env python virtual environment in shell:
	source crypto_api_env/bin/activate
3) cd into crypto_api_env/crypto_api to move to git repo.

'''


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

api_key = '231f04b7-44ce-4dcd-8dfd-0f0e0e1fbda4'

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
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
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  
