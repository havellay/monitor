import from googlefinance import getQuotes as g_get_quotes
from Report import db
from Attribute import attribute_dict

"""
There is a bit of redundancy wrt how many instances of the symbol strings
exist (stored in an obj as well as used in dict etc.
This is intentional. For now, this gives better design to use either Google
or Yahoo when fetching prices. This may change in the future.
The idea is that we don't differentiate the prices fetched from one service
from those fetched from another. Having 1 months data from one service and
another month's from another service should be possible and easy.
"""

g_symbol_dict = {}
y_symbol_dict = {}

symbol_dict   = g_symbol_dict   # Using g_symbol_dict as our go to dict
                                # for now. This may have to change later

class Symbol():
    self.name       = ''    # There is probably no way of getting this
    self.g_symbol   = ''
    self.y_symbol   = ''
    self.known_attrib_dict  = {}

    def __init__(self, name='', g_symbol='', y_symbol=''):
        global g_symbol_dict, y_symbol_dict

        self.name       = name
        self.g_symbol   = g_symbol
        self.y_symbol   = y_symbol

        g_symbol_dict[g_symbol] = self
        y_symbol_dict[y_symbol] = self
        
        return self

    @staticmethod
    def lookup_by_symbol(symbol='', service='g'):
        symbol_dict = g_symbol_dict

        if service == 'y':
            symbol_dict = y_symbol_dict

        query_symbol = symbol_dict.get(symbol)
        if query_symbol is None:
                try:
                    if service == 'g':
                        g_get_quotes(symbol)
                    else:
                        raise YahooError('Yahoo hasn\'t been implemented yet')
                    query_symbol = symbol_dict[symbol] = Symbol(g_symbol=symbol)
                except urllib2.HTTPError:
                    print('{symbol} is invalid'.format(symbol=symbol))
        return query_symbol

    def get_attrib(self, s_attrib):
        """
        TODO : perform all dict gets in the right way. No more check if None
                etc; instead find the recommended access method and replace
        """
        """
        NOTE :
         - attribute is a string, get the particular attribute object
            and pass the symbol's object to it; it will get the prices
            and compute the attribute's values
        """
        existing_attrib = self.known_attrib_dict.get(s_attrib)

        if existing_attrib is None:
            new_attrib = attribute_dict.get(s_attrib)
            if new_attrib is None:
                # This attribute hasn't been defined yet
            else:
                self.known_attrib_dict[s_attrib] = new_attrib.calculate(self)
                existing_attrib = self.known_attrib_dict.get(s_attrib)
                            # calculate() takes a symbol and returns the attribute
                            # instance
        return existing_attrib

