import requests
import json

from yahoo_finance import Share as yHandle

class NSE_picker(object):
  url = 'http://nseindia.com//live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol={symbol}'

  @staticmethod
  def get_current_price_volume(symbol=None):
    symbol  = symbol.nse_symbol
    try:
      info_string = requests.get(
          NSE_picker.url.format(symbol=symbol)).content
      info_dict   = json.loads(info_string)
      return (
          float(info_dict['data'][0]['lastPrice'].replace(',','')),
          float(info_dict['data'][0]['quantityTraded'].replace(',','')),
        )
    except Exception:
      print 'some problem occurred'
      return None

  @staticmethod
  def get_historical_price(symbol=None, from_date=None, to_date=None):
    return None


class Yahoo_picker(object):
  @staticmethod
  def get_current_price_volume(symbol=None):
    return None

  @staticmethod
  def get_historical_price(symbol=None, from_date=None, to_date=None):
    symbol      = symbol.y_symbol
    handle      = yHandle(symbol)
    new_quotes  = handle.get_historical(
        from_date.__str__(), to_date.__str__())[::-1]
    """
      This is an example for 'RELIANCE.NS'
        {'Adj_Close': '928.906',
         'Close': '948.25',
         'Date': '2014-04-25',
         'High': '969.00',
         'Low': '946.00',
         'Open': '968.00',
         'Symbol': 'RELIANCE.NS',
         'Volume': '3029200'},
        {'Adj_Close': '947.421',
         'Close': '967.15',
         'Date': '2014-04-24',
         'High': '967.15',
         'Low': '967.15',
         'Open': '967.15',
         'Symbol': 'RELIANCE.NS',
         'Volume': '000'},
      The above prices are in descending order of
      date; by inverting the list, we get it in
      ascending order of date
    """
    return new_quotes

class Picker(object):
  intraday_picker    = NSE_picker
  historical_picker  = Yahoo_picker

  @staticmethod
  def get_current_price_volume(symbol=None):
    return Picker.intraday_picker.get_current_price_volume(symbol)

  @staticmethod
  def get_historical_price(symbol=None, from_date=None, to_date=None):
    return Picker.historical_picker(symbol, from_date, to_date)
