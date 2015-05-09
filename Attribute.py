from datetime import date, timedelta

import Global

class Attribute():
  def get_name(self):
    return None
  def calculate(self, symbol):
    return None

class RSI(Attribute):
  root_name     = 'RSI'
  name          = ''
  default_opts  = {}
  rsi_list      = []
  moving_avg    = 1     # 1 -> EMA, 2 -> SMA

  def __init__(self):
    """
    NOTE :
        default_opts['period']  = 5 could mean a week
        default_opts['param']   = 15 would be a smoother curve

    """
    self.default_opts['period']      = 1         # meaning 1 day
    self.default_opts['param']       = 10        # consider 10 days worth
    self.default_opts['date_delta']  = timedelta(weeks=52)   # 52 weeks
    self.default_opts['to_date']     = date.today()
    self.default_opts['from_date']   = (
        self.default_opts['to_date'] - self.default_opts['date_delta']
      )
    self.name   = (
        self.name+'_period_'+str(self.default_opts['period'])+
        '_param_'+str(self.default_opts['param'])
      )
    # TODO : should call calculate right away : if not, then the
    #   here indicating the from_date and to_date would be inaccurate
    #   because the data would not have been calculated
    return None

  def __str__(self):
    return self.name

  def options(self, options_str):
    opts  = {}
    list_of_opts_to_get = [
        ('period', int),
        ('param', int),
        ('date_delta', date),
        ('to_date', date),
        ('from_date', date),
      ]
    for opt,typ in list_of_opts_to_get:
      if opt in options_str:
        opts[opt] = str_to_typ(get_param(options_str, opt),typ)
      else:
        opts[opt] = self.default_opts[opt]
    return opts

  def get_RSI(self, quotes, opts):
    """ Returns a list of tuples
      - each tuple is an RSI value [0] and a date [1]
    """
    rsi_list    = []
    av_gain     = 0.0
    av_loss     = 0.0

    if self.moving_avg == 1:
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

  def calculate(self, symbol=None, options=None):
    """
    NOTE :
    - default is to try and calculate for a year
    """
    opts = options or self.default_opts

    if symbol.is_attribute_known(self.name):
      available_from, available_to = symbol.attribute_known_for(self.name)
      opts['from_date'] = (
          available_from if available_from < opts['from_date'] 
            else opts['from_date']
        )
      opts['to_date']   = (
          available_to if available_to > opts['to_date']
            else opts['to_date']
        )

    data_from_date = (opts.get('from_date')
                        - timedelta(days=(opts.get('param')-2)))
    quotes_list = symbol.get_quotes(
        data_from_date,
        opts.get('to_date')
      )

    self.rsi_list = self.get_RSI(quotes_list, opts)

    Global.globe.things_to_plot.append(self.rsi_list)

    # need to write rsi_list to a file
    symbol.write_attrib_to_file(self.name, self.rsi_list)

    # override the default_opts with the from and to dates in opts
    self.default_opts['from_date']  = opts['from_date']
    self.default_opts['to_date']    = opts['to_date']

    return self

  def known_for(self):
    return (self.default_opts['from_date'], self.default_opts['to_date'])

  def is_triggered(self, trigger_val, bias):
    trigger_val = float(trigger_val)
    if bias == '+':
      if self.rsi_list[-1][0] > trigger_val:
        return (True, self.rsi_list[-1])
    if bias == '-':
      if self.rsi_list[-1][0] <= trigger_val:
        return (True, self.rsi_list[-1])
    return (False, 0)

def get_param(opts_str, opt):
  start_from  = opts_str.index(opt+'_')+len(opt+'_')
  if '_' in opts_str[start_from:]:
    end_at      = opts_str[start_from:].index('_')
    return opts_str[start_from:start_from+end_at]
  else:
    return opts_str[start_from:]

def str_to_typ(string, typ):
  if typ is int:
    return int(string)
  elif typ is date:
    return datetime.strptime(string, '%Y-%m-%d').date()
  return None
