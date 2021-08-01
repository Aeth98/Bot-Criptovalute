import requests
from pprint import pprint
import time
from datetime import datetime


class Bot:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': '100',
            'convert': 'usd'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '22c4a1f0-898a-4897-9cb6-6a7c46c1a988'
        }

    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return r['data']


impactbot = Bot()
orders = []
amount = 1
number_currencies_bought = 0
order_in_market = False
while(1):
    percent_change = 0
    currencies_watchlist = 0
    now = datetime.now()
    minutes = 10
    seconds = 60 * minutes
    currencies = impactbot.fetchCurrenciesData()
    if order_in_market == False:
        for currency in currencies:
            if currency['quote']['USD']['percent_change_1h'] > 1 and currency['quote']['USD']['percent_change_1h'] > percent_change :
                details_order = {
                    'date': now,
                    'currency': currency['symbol'],
                    'operation': 'buy',
                    'amount': amount,
                    'price': currency['quote']['USD']['price'],
                    'stoploss': currency['quote']['USD']['price'] - 0.01 * currency['quote']['USD']['price'],
                }
                currencies_watchlist = currencies_watchlist + 1
        if currencies_watchlist > 4:
            orders.append(details_order)
            print('Operazione eseguita\nDettagli transazione: \n')
            pprint(orders[number_currencies_bought])
            order_in_market = True
        else:
            print("Non c'erano almeno 5 crypto con una varazione percentuale maggiore di 1")
    time.sleep(seconds)
    for currency in currencies:
        if currency[symbol] == orders[number_currencies_bought]['currency'] and orders[number_currencies_bought]['stoploss'] <= currency['quote']['USD']['price']:
            order_in_market = False
    number_currencies_bought = number_currencies_bought + 1

