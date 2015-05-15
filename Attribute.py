from datetime import date, timedelta
from Plotter import Plotter

class Attribute(object):
  attrib_dict = {}

  @staticmethod
  def get_attrib_dict():
    return Attribute.attrib_dict

  def options_from_str(self, opts_str=''):
    for opt,typ in self.list_of_opts_to_get:
      if opt in opts_str:
        self.opts[opt] = str_to_typ(self.get_param(opts_str, opt), typ)
    self.update_name()
    return self.opts

class Price(Attribute):
  root_name = 'Price'
  def __init__(self):
    self.name       = 'Price_'
    self.opts       = {}
    self.price_list = []

    self.opts['datedelta']  = timedelta(weeks=52)   # 52 weeks
    self.opts['todate']     = date.today()
    self.opts['fromdate']   = (
        self.opts['todate'] - self.opts['datedelta']
      )
    self.opts['symbolmode'] = 'EoD'
    self.list_of_opts_to_get  = [
        ('datedelta', date),
        ('todate', date),
        ('fromdate', date),
        ('symbolmode', str),
      ]
    self.update_name()
    return None

  def update_name(self):
    self.name = self.root_name+'_symbolmode_'+str(self.opts['symbolmode'])
    return self.name

  def __str__(self):
    return self.name

  def calculate(self, symbol=None):
    quotes_list = symbol.get_EoD_quotes(
        self.opts.get('fromdate'),
        self.opts.get('todate')
      )

    self.price_list = quotes_list

    Plotter.get_plot_buffer().append((self.name, self.price_list))

    return self

  def is_triggered(self, trigger_val=None, bias=None):
    return (True, 0)

  def known_for(self):
    """
    THIS IS PROBABLY WRONG
    """
    return (self.opts['fromdate'], self.opts['todate'])


class RSI(Attribute):
  root_name     = 'RSI'

  def __init__(self):
    """
    NOTE :
        opts['period']  = 5 could mean a week
        opts['param']   = 15 would be a smoother curve

    """
    self.name          = ''
    self.rsi_list      = []

    self.opts               = {}
    self.opts['period']     = 1         # meaning 1 day
    self.opts['param']      = 10        # consider 10 days worth
    self.opts['datedelta']  = timedelta(weeks=52)   # 52 weeks
    self.opts['todate']     = date.today()
    self.opts['fromdate']   = (
        self.opts['todate'] - self.opts['datedelta']
      )
    self.opts['symbolmode'] = 'EoD'
    self.opts['movingavg']  = 'EMA'
    self.update_name()

    self.list_of_opts_to_get = [
        ('period', int),
        ('param', int),
        ('datedelta', date),
        ('todate', date),
        ('fromdate', date),
        ('symbolmode', str),
      ]
    return None

  def update_name(self):
    self.name   = (
        self.root_name+
          '_period_'+str(self.opts['period'])+
          '_param_'+str(self.opts['param'])+
          '_symbolmode_'+str(self.opts['symbolmode'])
      )
    return self.name

  def __str__(self):
    return self.name

  def get_RSI(self, quotes=None):
    """ Returns a list of tuples
      - each tuple is an RSI value [0] and a date [1]
    """
    opts  = self.opts

    if len(quotes) < opts.get('param'):
      # we don't have enough values
      return [(0,0)]

    rsi_list    = []
    av_gain     = 0.0
    av_loss     = 0.0

    if opts.get('movingavg') == 1:
      multiplier  = (2.0/(opts.get('param')+1))
    else:
      multiplier  = 1.0/opts.get('param')

    for x in xrange(opts.get('param')):
      quote_diff = float(quotes[x][0]) - float(quotes[x-1][0])
      if quote_diff > 0:
        av_gain += quote_diff
      else:
        av_loss += quote_diff

    av_gain = 1.0 * av_gain / opts.get('param')
    av_loss = 1.0 * av_loss / opts.get('param')
    rs  = av_gain / (-1*av_loss)
    rsi_list.append((100 - 100/(1+rs), quotes[opts.get('param')-1][1]))

    for x in xrange(opts.get('param'), len(quotes)):
      quote_diff = float(quotes[x][0]) - float(quotes[x-1][0])
      if quote_diff > 0:
        av_gain = multiplier*quote_diff + (1-multiplier)*av_gain
      else:
        av_loss = multiplier*quote_diff + (1-multiplier)*av_loss
      rs = av_gain / (-1*av_loss)
      rsi_list.append((100 - 100/(1+rs), quotes[x][1]))

    return rsi_list

  def calculate(self, symbol=None):
    """
    TODO : A lot of things in this method and methods stemming from this
            will change when we store data in a database instead of
            pickling them; make the code better when that happens
    """
    opts = self.opts

    quotes_list = None

    if opts.get('symbolmode') == 'EoD':
      if symbol.is_attribute_known(self.name):
        available_from, available_to = symbol.attribute_known_for(self.name)
        opts['fromdate'] = (
            available_from if available_from < opts['fromdate'] 
              else opts['fromdate']
          )
        opts['todate']   = (
            available_to if available_to > opts['todate']
              else opts['todate']
          )

      data_fromdate = (opts.get('fromdate')
                          - timedelta(days=(opts.get('param')-2)))
      quotes_list = symbol.get_EoD_quotes(data_fromdate, opts.get('todate'))

    elif opts.get('symbolmode') == 'intraday':
      quotes_list = symbol.get_intraday_quotes()
      pass

    self.rsi_list = self.get_RSI(quotes_list)

    Plotter.get_plot_buffer().append((self.name, self.rsi_list))

    # need to write rsi_list to a file
    symbol.write_attrib_to_file(self.name, self.rsi_list)

    return self

  def known_for(self):
    return (self.opts['fromdate'], self.opts['todate'])

  def is_triggered(self, trigger_val=None, bias=None):
    trigger_val = float(trigger_val)
    if bias == '+':
      if self.rsi_list[-1][0] > trigger_val:
        return (True, self.rsi_list[-1])
    if bias == '-':
      if self.rsi_list[-1][0] <= trigger_val:
        return (True, self.rsi_list[-1])
    return (False, 0)

  @staticmethod
  def get_param(opts_str='', opt=None):
    start_from  = opts_str.index(opt+'_')+len(opt+'_')
    if '_' in opts_str[start_from:]:
      end_at      = opts_str[start_from:].index('_')
      return opts_str[start_from:start_from+end_at]
    else:
      return opts_str[start_from:]

def str_to_typ(string='', typ=None):
  if typ is int:
    return int(string)
  elif typ is str:
    return string
  elif typ is date:
    return datetime.strptime(string, '%Y-%m-%d').date()
  return None

Attribute.attrib_dict['Price']  = Price
Attribute.attrib_dict['RSI']  = RSI
