import cPickle as pickle
import datetime

from db_comm import Queries

# google doesn't have historical prices of indian shares, Pity
from googlefinance import getQuotes as g_get_quotes
from google import GoogleQuote

# yahoooooo
from yahoo_finance import Share

import Report
import Global

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

symbol_dict   = y_symbol_dict   # Using g_symbol_dict as our go to dict
                                # for now. This may have to change later

class Symbol():
  name         = ''    # There is probably no way of getting this
  g_symbol     = ''
  y_symbol     = ''
  attrib_dict  = {}
  in_mem_db    = []

  def __init__(self, name='', g_symbol='', y_symbol=''):
    global g_symbol_dict, y_symbol_dict

    self.name       = name
    self.g_symbol   = g_symbol
    self.y_symbol   = y_symbol

    if g_symbol:
      g_symbol_dict[g_symbol] = self
    if y_symbol:
      y_symbol_dict[y_symbol] = self

    return None

  @staticmethod
  def lookup_by_symbol(symbol='', service='y'):
    global symbol_dict
    symbol_dict = y_symbol_dict

    if service == 'g':
      symbol_dict = g_symbol_dict

    query_symbol = symbol_dict.get(symbol)

    if query_symbol is None:
      try:
        if service == 'g':
          g_get_quotes(symbol)
          query_symbol  = Symbol(g_symbol=symbol)
        elif service == 'y':
          y_obj = Share(symbol)
          if 'start' not in y_obj.get_info():
            raise Exception('Given symbol doesn\'t exist in Yahoo finance')
          query_symbol  = Symbol(y_symbol=symbol)
      except urllib2.HTTPError:
        print('{symbol} is invalid'.format(symbol=symbol))
      except Exception as e:
        print(e.args)

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
    existing_attrib = self.attrib_dict.get(s_attrib)

    if existing_attrib is None:
      attrib_root_name  = s_attrib[0:s_attrib.index('_')]
      new_attrib        = Global.globe.attrib_dict.get(attrib_root_name)()
      if new_attrib is None:
        # This attribute hasn't been defined yet
        pass
      else:
        self.attrib_dict[s_attrib] = new_attrib.calculate(
            symbol=self,
            options=new_attrib.options(
                period=1,
                param=10,
              )
          )
        existing_attrib = self.attrib_dict.get(s_attrib)
    return existing_attrib

  def is_attribute_known(self, s_attrib):
    return (self.attrib_dict.get(s_attrib) != None)

  def attribute_known_for(self, s_attrib):
    return self.attrib_dict.get(s_attrib).known_for()

  def get_quotes(self, from_date, to_date):
    # qdt_list -> quote_date_tuple_list
    qdt_list, get_more, from_date, to_date = self.known_quotes(from_date, to_date)
    if get_more is True:
      qdt_list.extend(self.ext_fetch_quotes(from_date, to_date))
    return qdt_list

  def known_quotes(self, from_date, to_date):
    qdt_list  = []
    get_more  = False

    # getting the file name that has the stock's quotes
    cursor  = Global.globe.db.cursor()
    Queries.s_filename_f_quotetab_w_symbol_eq(cursor, self.name)
    quote_file_name = cursor.fetchone()

    if not quote_file_name:
      # no file representing this symbol exists now;
      get_more  = True
      return qdt_list, get_more, from_date, to_date

    # prices will be stored in a pickle, read from the file
    quotes_dict_list= pickle.load(open(quote_file_name+'.pickle','r'))

    for line in quotes_rnc:
      qdt_list.append((
          line.get('Close'),            # 0 : closing price
          datetime.datetime.strptime(   # 1 : date
              line.get('Date'),'%Y-%m-%d'
            ).date(),
        ))

    from_date_index = to_date_index = 0

    for x in xrange(len(qdt_list)):
      if qdt_list[x][1] == from_date:
        from_date_index = x
        break
      if qdt_list[x][1] == to_date:
        to_date_index   = x
        break

    if to_date_index != 0:
      for x in xrange(from_date_index, len(qdt_list)):
        if qdt_list[x][1] == to_date:
          to_date_index = x
          break

    if from_date_index == 0 and to_date_index == 0:
      get_more  = True
    elif from_date_index == 0:
      get_more  = True
      to_date   = qdt_list[0][1]
    elif to_date_index == 0:
      get_more  = 0
      from_date = qdt_list[-1][1]

    return qdt_list, get_more, from_date, to_date

  def ext_fetch_quotes(self, from_date, to_date):
    qdt_list = []

    # fetch quotes from the Internet
    new_quotes  = Share(self.y_symbol).get_historical(
                    from_date.__str__(), to_date.__str__())[::-1]

    # getting the file name that has the stock's quotes
    cursor  = Global.globe.db.cursor()
    Queries.s_filename_f_quotetab_w_symbol_eq(cursor, self.name)
    quote_file_name     = cursor.fetchone()

    existing_quotes = []
    if quote_file_name:
      # read stuff from the file
      existing_quotes.extend(pickle.load(open(quote_file_name+'.pickle', 'r')))
    else:
      quote_file_name = 'data/'+self.y_symbol

    # merge with stuff fetched from the internet
    merged_quotes = merge_quotes(existing_quotes, new_quotes)

    pickle.dump(merged_quotes, open(quote_file_name+'.pickle','w'))

    for line in merged_quotes:
      qdt_list.append((
          line.get('Close'),                # 0 : closing price
          datetime.datetime.strptime(       # 1 : date
              line.get('Date'),'%Y-%m-%d'
            ).date(),
        ))

    return qdt_list

  def write_attrib_to_file(self, attrib_name, attrib_vals):
    file_name = 'data/'+self.name+'_'+attrib_name
    pickle.dump(attrib_vals, open(file_name+'.pickle', 'w'))
    return None

def csv_into_rows_and_cols(file_name=None, data=None):
  if file_name:
    f         = open(file_name, 'r')
    data  = f.read()
  data  = data or data.split('\n')
  for i in xrange(len(data)):
    data[i] = data[i].split(',')
  return data

def merge_quotes(qrnc_1, qrnc_2):
  if len(qrnc_1) == 0:
    return qrnc_2
  i = j = 0
  merged  = []
  for x in xrange(len(qrnc_1)+len(qrnc_2)):
    date_qrnc_1 = datetime.datetime.strptime(
                          qrnc_1[i]['Date'],'%Y-%m-%d').date()
    date_qrnc_2 = datetime.datetime.strptime(
                          qrnc_2[j]['Date'],'%Y-%m-%d').date()
    if date_qrnc_1 < date_qrnc_2:
      merged.extend([date_qrnc_1,date_qrnc_2])
      i += 1
    elif date_qrnc_1 > date_qrnc_2:
      merged.extend([date_qrnc_2,date_qrnc_1])
      j += 1
    else:
      merged.append(date_qrnc_1)
      i += 1
      j += 1
  return merged
