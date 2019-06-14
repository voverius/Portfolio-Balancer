import json
import time
from urllib.request import Request, urlopen
from urllib.parse import urlencode

# Possible Commands
public_commands = ['returnTicker', 'return24hVolume', 'returnOrderBook', 'returnTradeHistory',
                   'returnChartData', 'returnCurrencies', 'returnLoanOrders']


class Poloniex:
    def __init__(self, APIKey='', Secret=''):
        self.APIKey = APIKey.encode()
        self.Secret = Secret.encode()

        # Public Commands
        self.CoinStatus = self.api('returnCurrencies')
        self.MarketTicker = self.api('returnTicker')
        self.MarketVolume = self.api('return24hVolume')
        self.MarketOrders = self.api('returnOrderBook', {'currencyPair': 'all', 'depth': 10})

        self.MarketLoans = lambda coin: self.api('returnLoanOrders', {'currency': coin})
        self.MarketTradeHistory = lambda pair: self.api('returnTradeHistory', {'currencyPair': pair})
        self.MarketChart = lambda pair, period=(60*60*24), start=time.time()-(60*60*24*7), end=time.time():\
            self.api('returnChartData', {'currencyPair': pair, 'period': period, 'start': start, 'end': end})
        self.MarketOrders = lambda pair='all', depth=10: \
            self.api('returnOrderBook', {'currencyPair': pair, 'depth': depth})

    def api(self, command, args={}):
        """
        returns 'False' if invalid command or if no APIKey or Secret is specified (if command is "private")
        returns {"error":"<error message>"} if API error
        """
        if command in public_commands:
            url = 'https://poloniex.com/public?'
            args['command'] = command
            ret = urlopen(Request(url + urlencode(args)))
            return json.loads(ret.read().decode(encoding='UTF-8'))
        else:
            return False


