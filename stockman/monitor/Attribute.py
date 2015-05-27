import cPickle as pickle
import json
import os

from stockman.settings import BASE_DIR
from monitor.models.Symbol import Symbol
from monitor.models.EoD import EoD
from monitor.models.Intraday import Intraday

class RSI(object):
  """
  If we choose to change the earliest available date,
  all pickle files should be deleted;
  """
  def __init__(self):
    self.values = []  # symbol's calculated attribs in
                      # ascending order of date
    return None

  def set_options(self, options):
    self.options  = options
    self.values   = [0]*options.get('time_param')
    return None

  def find_RSI(self, quotes):
    if len(self.values) > 0:
      # getting rid of quotes that we needn't bother about
      # because values for those quotes are already available
      start_from  = len(self.values)+self.options.get('time_param')-1
      quotes      = quotes[start_from:]

    if len(quotes) < self.options.get('time_param'):
      return None

    av_gain = 0.0
    av_loss = 0.0

    if 1 == 1:        # using exponential moving average
      multiplier  = (2.0/(self.options.get('time_param')+1))
    else:
      multiplier  = (1.0/self.options.get('time_param'))

    for x in xrange(self.options.get('time_param')):
      quote_diff  = float(quotes[x]) - float(quotes[x-1])
      if quote_diff > 0:
        av_gain   += quote_diff
      else:
        av_loss   += quote_diff

    av_gain = 1.0 * av_gain / self.options.get('time_param')
    av_loss = 1.0 * av_loss / self.options.get('time_param')
    rs      = av_gain / (-1*av_loss)
    self.values.append(100 - 100/(1+rs))

    for x in xrange(self.options.get('time_param'), len(quotes)):
      quote_diff  = float(quotes[x]) - float(quotes[x-1])
      if quote_diff > 0:
        av_gain = multiplier*quote_diff + (1-multiplier)*av_gain
      else:
        av_loss = multiplier*quote_diff + (1-multiplier)*av_loss
      rs    = av_gain / (-1*av_loss)
      self.values.append(100 - 100/(1+rs))

    return None

  def calculate(self):
    quotes  = []
    symbol  = Symbol.objects.filter(id=self.options.get('symbol_id'))
    if self.options.get('time_unit') == 'day':     # EoD
      for entry in EoD.objects.filter(symbol=symbol):
        quotes.append(entry.close_qt)
    else:                                     # Intraday
      for entry in Intraday.objects.filter(symbol=symbol):
        quotes.append(entry.quote)
    self.find_RSI(quotes)
    return None

  def is_triggered(self, trigger):
    if trigger.bias == '+' and self.values[-1] > trigger.trig_val:
      return (True, self.values[-1])
    if trigger.bias == '-' and self.values[-1] <= trigger.trig_val:
      return (True, self.values[-1])
    return (False, 0)

class Attribute(object):
  directory = {
      'RSI':RSI,
    }
  @staticmethod
  def is_triggered(trigger):
    reminder  = trigger.reminder
    symbol    = trigger.symbol
    attrib    = trigger.attrib
    trig_val  = trigger.trig_val
    bias      = trigger.bias

    """
    converting the 'attrib' string to json would
    produce a dict like the following :
      attrib_info.get('root_name')  -> 'RSI'
      attrib_info.get('options')    ->  {
                                          'symbol_id':1,
                                          'time_unit':'day',
                                          'time_param':10
                                        }

    Each attribute should have a form that fetches
    details from the user and then produces a dict.
    Using this dict, we should be able to produce
    the attrib name string and backwards.
    """
    attrib_info_dict  = json.loads(attrib)

    file_name = BASE_DIR+'/pickles/'+str(symbol.id)+'_'+attrib+'.pickle'

    if os.path.isfile(file_name):
      # 'attrib_obj' is an instance of RSI() etc.
      attrib_obj  = pickle.load(open(file_name, 'r'))
    else:
      # compute the attrib and store in pickle
      attrib_obj  = Attribute.directory.get(attrib_info_dict.get('root_name'))()
      attrib_obj.set_options(attrib_info_dict.get('options'))

    attrib_obj.calculate()
    pickle.dump(attrib_obj, open(file_name, 'w'))
    return attrib_obj.is_triggered(trigger)

