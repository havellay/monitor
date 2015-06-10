import cPickle as pickle
import json
import os

from django import forms

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

  def check_is_triggered(self, trigger):
    # trig_val is a string because that is how the model describes it
    # convert to a float when comparing here; we don't need a try
    # except block because we have verified this conversion earlier
    # in to_clean_optd()
    trig_val  = float(trigger.trig_val)
    print '{trigger} current value is {val}'.format(
        trigger=trigger, val=self.values[-1]
      )
    if self.values[-1] == 0:    # this is not the right way to do things; fix this
      return (False, 0)
    if trigger.bias == '+' and self.values[-1] > trig_val:
      return (True, self.values[-1])
    if trigger.bias == '-' and self.values[-1] <= trig_val:
      return (True, self.values[-1])
    return (False, 0)

  @staticmethod
  def to_clean_optd(optd):
    c_optd  = {}
    key_type_dict = {
        'symbol_id': int,
        'time_param': int,
        'time_unit': str,
        'trig_val': float,
        'bias': str,
      }
    if optd.get('time_unit') == '---':
      return None
    for key in optd:
      if key_type_dict.get(key):
        try:
          c_optd[key] = key_type_dict.get(key)(optd.get(key))
        except Exception:
          print 'error when cleaning attribute options dict'
      else:
        c_optd[key] = optd.get(key)
    return c_optd

  @staticmethod
  def optd_to_file_name(optd):
    # {
    #     "root_name": "RSI",
    #     "options":
    #     {
    #         "symbol_id": 1,
    #         "time_param": 10,
    #         "time_unit": "day"
    #     }
    # }
    temp_optd = {}
    temp_optd['root_name']  = optd.get('attribute')
    temp_optd['options']    = {}
    temp_optd['options']['symbol_id']   = optd.get('symbol_id')
    temp_optd['options']['time_param']  = optd.get('time_param')
    temp_optd['options']['time_unit']   = optd.get('time_unit')
    return json.dumps(temp_optd)

  class form(forms.Form):
    # Trigger form is used when creating a Reminder;
    # so, it has fields such as 'bias'
    root_name   = 'RSI'
    choices     = [
        ('---', '---'),
        ('day','day'),
        ('minute','minute'),
      ]
    bias_choices= [
        ('---', '---'),
        ('+', '+'),
        ('-', '-'),
      ]
    time_unit   = forms.ChoiceField(choices=choices)
    time_param  = forms.IntegerField()
    bias        = forms.ChoiceField(choices=bias_choices)
    trig_val    = forms.DecimalField()
    time_unit.widget.attrs["onchange"]  = (
        'make_attribute_string(this, \'time_unit\');'
      )
    time_param.widget.attrs["onchange"] = (
        'make_attribute_string(this, \'time_param\');'
      )
    bias.widget.attrs["onchange"] = (
        'make_attribute_string(this, \'bias\');'
      )
    trig_val.widget.attrs["onchange"]  = (
        'make_attribute_string(this, \'trig_val\');'
      )


class Attribute(object):
  directory = {
      'RSI':RSI,
      'self':RSI,
    }
  @staticmethod
  def check_is_triggered(trigger):
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
    file_name = file_name.replace(' ','')

    if os.path.isfile(file_name):
      # 'attrib_obj' is an instance of RSI() etc.
      attrib_obj  = pickle.load(open(file_name, 'r'))
    else:
      # compute the attrib and store in pickle
      attrib_obj  = Attribute.directory.get(attrib_info_dict.get('root_name'))()
      attrib_obj.set_options(attrib_info_dict.get('options'))

    attrib_obj.calculate()
    pickle.dump(attrib_obj, open(file_name, 'w'))
    return attrib_obj.check_is_triggered(trigger)

  # NOTE: thought of taking the common lines from
  # to_clean_optd() and get_form() using
  # vars(attrib) as a dict to get the method;
  # but this wouldn't shorten the methods.
  @staticmethod
  def to_clean_optd(optd):
    attrib  = Attribute.directory.get(optd.get('attribute'))
    if attrib:
      return attrib.to_clean_optd(optd)
    return None

  @staticmethod
  def get_form(attribs):
    attrib  = Attribute.directory.get(attribs)
    if attrib:
      return attrib.form()
    return None

  @staticmethod
  def optd_to_file_name(optd):
    attrib = Attribute.directory.get(optd.get('attribute'))
    if attrib:
      return attrib.optd_to_file_name(optd)
    return None

