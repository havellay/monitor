import requests
import json

from yahoo_finance import Share as yHandle

class NSE_picker(object):
  url = 'http://nseindia.com//live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol={symbol}'

  @staticmethod
  def get_current(symbol=None):
    symbol  = symbol.nse_symbol
    try:
      info_string = requests.get(
          NSE_picker.url.format(symbol=symbol)).content
      info_dict   = json.loads(info_string)
      return {
          'open':float(0),
          'close':float(info_dict['data'][0]['lastPrice'].replace(',','')),
          'high':float(0),
          'low':float(0),
          'quote':float(info_dict['data'][0]['lastPrice'].replace(',','')),
          'volume':float(info_dict['data'][0]['quantityTraded'].replace(',','')),
        }
    except Exception:
      print 'some problem occurred'
      return None

  @staticmethod
  def get_historical(symbol=None, from_date=None, to_date=None):
    return None


class Yahoo_picker(object):
  @staticmethod
  def get_current(symbol=None):
    return None

  @staticmethod
  def get_historical(symbol=None, from_date=None, to_date=None):
    symbol      = symbol.y_symbol
    handle      = yHandle(symbol)
    import ipdb; ipdb.set_trace()
    quotes_dict_list = handle.get_historical(
        from_date.__str__(), to_date.__str__())[::-1]
    """
      This is an example for 'RELIANCE.NS' as in quotes_dict_list
        {'Adj_Close': '928.906',
         'Close': '948.25',     -> close_qt
         'Date': '2014-04-25',
         'High': '969.00',      -> high_qt
         'Low': '946.00',       -> low_qt
         'Open': '968.00',      -> open_qt
         'Symbol': 'RELIANCE.NS',
         'Volume': '3029200'},  -> volume
        {'Adj_Close': '947.421',
         'Close': '967.15',
         'Date': '2014-04-24',
         'High': '967.15',
         'Low': '967.15',
         'Open': '967.15',
         'Symbol': 'RELIANCE.NS',
         'Volume': '000'},
    """
    new_dict_list    = []
    for qt in quotes_dict_list:
      new_dict_list.append(
          {
            'close_qt':qt.get('Close'),
            'high_qt' :qt.get('High'),
            'low_qt'  :qt.get('Low'),
            'open_qt' :qt.get('Open'),
            'volume'  :qt.get('Volume'),
          },
        )
    return new_dict_list

class Picker(object):
  intraday_picker    = NSE_picker
  historical_picker  = Yahoo_picker

  @staticmethod
  def get_current(symbol=None):
    return Picker.intraday_picker.get_current(symbol)

  @staticmethod
  def get_historical(symbol=None, from_date=None, to_date=None):
    return Picker.historical_picker.get_historical(symbol, from_date, to_date)
