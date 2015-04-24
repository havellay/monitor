import from googlefinance import getQuotes as g_get_quotes

# the following import statement might not work; check
from db_comm import my_db_obj

# there should be a list of symbols - a company that has >=1 reminder set for
# it should be included in this list
g_symbol_list = {}
y_symbol_list = {}

class Symbol():
    self.name       = ''    # There is probably no way of getting this
    self.g_symbol   = ''
    self.y_symbol   = ''

    def __init__(self, name='', g_symbol='', y_symbol=''):
        self.name       = name
        self.g_symbol   = g_symbol
        self.y_symbol   = y_symbol

    @staticmethod
    def lookup_by_symbol(symbol='', service='g'):
        symbol_list = g_symbol_list

        if service == 'y':
            symbol_list = y_symbol_list

        query_symbol = symbol_list.get(symbol)
        if query_symbol is None:
                try:
                    if service == 'g':
                        g_get_quotes(symbol)
                    else:
                        raise YahooError('Yahoo hasn\'t been implemented yet')
                    query_symbol = symbol_list[symbol] = Symbol(g_symbol=symbol)
                except urllib2.HTTPError:
                    print('{symbol} is invalid'.format(symbol=symbol))
        return query_symbol

    def update_data(self):
        get_db.
