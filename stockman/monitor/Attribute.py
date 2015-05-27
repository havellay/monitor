import cPickle as pickle

from stockman.settings import BASE_DIR

class Attribute(object):
  directory = {
      # 'RSI':RSI,
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
      attrib_info.get('options')    -> {'time_unit':'day', 'time_param':10}

    Each attribute should have a form that fetches
    details from the user and then produces a dict.
    Using this dict, we should be able to produce
    the attrib name string and backwards.
    """
    attrib_info_dict  = json.loads(attrib)

    file_name = BASE_DIR+'/'+symbol.id+'_'+attrib+'.pickle'

    if os.path.isfile(file_name):
      # 'attrib_obj' is an instance of RSI() etc.
      attrib_obj  = pickle.load(open(file_name, 'r'))
      attrib_obj.calculate()
    else:
      # compute the attrib and store in pickle
      attrib_obj  = Attribute.directory.get(attrib_info_dict.get('root_name'))()
      attrib_obj.set_options(attrib_info_dict.get('options'))

    attrib_obj.calculate()
    pickle.dump(attrib_obj, open(file_name, 'w'))
    return attrib_obj.is_triggered(trigger)
