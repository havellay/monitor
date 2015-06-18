import requests
import json
from datetime import datetime

from yahoo_finance import Share

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
          'open'  :float(0),
          'close' :float(info_dict['data'][0]['lastPrice'].replace(',','')),
          'high'  :float(0),
          'low'   :float(0),
          'quote' :float(info_dict['data'][0]['lastPrice'].replace(',','')),
          'volume':float(
              info_dict['data'][0]['quantityTraded'].replace(',','')),
          'time'  :datetime.strptime(
              info_dict['lastUpdateTime'], '%d-%b-%Y %H:%M:%S'),
        }
    except Exception as e:
      print 'NSE_picker : get_current : some problem occurred'
      print e
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
    done = False
    while not done:
      try:
        handle = Share(symbol.y_symbol)
        quotes_dict_list = handle.get_historical(
            from_date.__str__(), to_date.__str__())[::-1]
        done = True
      except Exception as e:
        print "Yahoo picker : get_historical : something bad happened"
        print e
        continue
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
            'close_qt':float(qt.get('Close')),
            'high_qt' :float(qt.get('High')),
            'low_qt'  :float(qt.get('Low')),
            'open_qt' :float(qt.get('Open')),
            'volume'  :int(qt.get('Volume')),
            'date'    :datetime.strptime(qt.get('Date'), '%Y-%m-%d'),
          },
        )
    return new_dict_list


class Google_picker(object):
  @staticmethod
  def get_current(symbol=None):
    return None

  @staticmethod
  def get_historical(symbol=None, from_date=None, to_date=None):
    # googlefinance 0.7 doesn't have a nice way of picking
    # historical quotes
    # the following is just nonsense from yahoo code
    handle      = Share(symbol.y_symbol)
    quotes_dict_list = handle.get_historical(
        from_date.__str__(), to_date.__str__())[::-1]
    new_dict_list    = []
    for qt in quotes_dict_list:
      new_dict_list.append(
          {
            'close_qt':float(qt.get('Close')),
            'high_qt' :float(qt.get('High')),
            'low_qt'  :float(qt.get('Low')),
            'open_qt' :float(qt.get('Open')),
            'volume'  :int(qt.get('Volume')),
            'date'    :datetime.strptime(qt.get('Date'), '%Y-%m-%d'),
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



