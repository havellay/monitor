from datetime import date, timedelta

class Attribute():
  name    = ''

  def get_name(self):
    return self.name

  def calculate(self, symbol):
    # base class knows nothing about calculate
    return None

class RSI(Attribute):
  root_name     = 'RSI'
  name          = ''
  default_opts  = {}
  rsi_list      = []
  moving_avg    = 2     # 1 -> EMA, 2 -> SMA

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
        self.name+'_period'+str(self.default_opts['period'])+
        '_param'+str(self.default_opts['param'])
      )
    # TODO : should call calculate right away : if not, then the
    #   here indicating the from_date and to_date would be inaccurate
    #   because the data would not have been calculated
    return None

  def __str__(self):
    return self.name

  def options(
      self, period=None, param=None, date_delta=None,
      to_date=None, from_date=None
    ):
    opts = {}
    opts['period']      = period    or self.default_opts['period']
    opts['param']       = param     or self.default_opts['param']
    opts['date_delta']  = date_delta or self.default_opts['date_delta']
    opts['to_date']     = to_date   or self.default_opts['to_date']
    opts['from_date']   = from_date or self.default_opts['from_date']

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

    data_from_date = opts.get('from_date') - timedelta(days=(opts.get('param')-2))
    quotes_list = symbol.get_quotes(
        data_from_date,
        opts.get('to_date')
      )

    self.rsi_list = self.get_RSI(quotes_list, opts)

    plot_this(self.rsi_list)

    # need to write rsi_list to a file
    symbol.write_attrib_to_file(self.name, self.rsi_list)

    # override the default_opts with the from and to dates in opts
    self.default_opts['from_date']  = opts['from_date']
    self.default_opts['to_date']    = opts['to_date']

    return self

  def known_for(self):
    return (self.default_opts['from_date'], self.default_opts['to_date'])

def plot_this(date_values_list):
  import matplotlib.pyplot as plt
  x_axis = []
  y_axis = []
  for y,x in date_values_list:
    x_axis.append(x)
    y_axis.append(y.__str__())
  plt.plot(x_axis, y_axis)
  plt.ylabel('RSI')
  plt.show()
