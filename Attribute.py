from datetime import date, timedelta

class Attribute():
  name    = ''

  def get_name(self):
    return self.name

  def calculate(self, symbol):
    # base class knows nothing about calculate
    return None

class RSI(Attribute):
  root_name       = 'RSI'
  name            = ''
  default_opts    = {}
  self.rsi_list   = []

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
        self.name+'_period'+str(defaut_opts['period'])+
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

    for x in xrange(opts.get('param')):
      quote_diff = quotes[x][0] - quotes[x-1][0]
      if quote_diff > 0:
        av_gain += quote_diff
      else:
        av_loss += quote_diff

    av_gain = 1.0 * av_gain / opts.get('param')
    av_loss = 1.0 * av_loss / opts.get('param')
    rs  = av_gain / av_loss
    rsi_list.append((100 - 100/(1+rs), quotes[opts.get('param')-1][1]))

    for x in xrange(opts.get('param'), len(quotes)):
      quote_diff = quotes[x][0] - quotes[x-1][0]
      if quote_diff > 0:
        av_gain = (1.0 * 
                (av_gain * (opts.get('param') - 1) + quote_diff) 
                / opts.get('param'))
      else:
        av_loss = (1.0 *
                (av_loss * (opts.get('param') - 1) + quote_diff)
                / opts.get('param'))
        rs = av_gain / av_loss
        rsi_list.append((100 - 100/(1+rs), quotes[x][1]))

    return rsi_list

  def calculate(self, symbol=None, options=None):
    """
    NOTE :
    - default is to try and calculate for a year
    """
    # maybe should make sure that all necessary parameteres
    #   are specified?
    opts = options or self.default_opts

    # NOTE about attribute_known_for ... if attribute hasn't been calculated
    # at all yet, then available_from should be maximum possible date and
    # available_to should be minimum possible date
    # 3 May : the above comment doesn't make sense; if the attribute is
    # present in the list of attributes that the symbol knows, it means
    # it has been calcualted at some point and has a valid from and to date
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

    # make sure that the data for the full duration that we are
    # interested in is available; if not, fetch it
    # NOTE about get_quotes() : 
    #   we need quotes from date before 'from_date' as well to calculate
    #   RSI. This will be the case for other tools as well, this is the
    #   responsiblity of the attribute's code to fetch prices for all days
    #   that it needs
    #   also, get_quotes should return a list
    # - The idea behind the '-2' in the following line is that we should
    #   account for weekends when calculating the number of days to get
    #   prices for.
    # - get_quotes() should return a list of tuples of the quotes and the
    #   date in string
    data_from_date = opts.get('from_date') - timedelta(days=opts.get('param')) - 2
    quotes_list = symbol.get_quotes(
        data_from_date,
        opts.get('to_date')
      )

    start_processing = False
    for x in xrange(len(quotes_list)):
      if (not start_processing and
          quotes_list[x][1] == data_from_date.today().strftime('%Y-%m-%d')):
        start_processing = True
      elif start_processing:
        self.rsi_list = get_RSI(quotes_list[x:], opts)
        break

    # need to write rsi_list to a file
    symbol.write_attrib_to_file(self.name, rsi_list)

    # override the default_opts with the from and to dates in opts
    self.default_opts['from_date']  = opts['from_date']
    self.default_opts['to_date']    = opts['to_date']

    return self

  def known_for(self):
    return (self.default_opts['from_date'], self.default_opts['to_date'])

# global_attrib_dict is used to access
# the root definition of attributes
global_attrib_dict = {
    'RSI': RSI,
  }
