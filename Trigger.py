from Symbol import symbol_dict

class Trigger():
  """
  NOTE :
   - `symbol`, `attribute`, `value` and `bias` are all strings
   - Symbol_dict.get(symbol).get_attrib(attribute).is_triggered(value, bias)
    the above is the ideal call;
  """
  self.s_symbol     = ''
  self.s_attribute  = ''
  self.s_value      = ''
  self.s_bias       = ''

  def __init__(self, s_symbol, s_attribute, s_value, s_bias):
    self.s_symbol     = symbol
    self.s_attribute  = attribute
    self.s_value      = value
    self.s_bias       = bias
    return True

  def __str__(self):
    return '{1} {2} {3} {4}'.format(s_symbol, s_attribute, s_value, s_bias)

  def is_triggered(self):
    return symbol_dict.get(symbol).get_attrib(attribute).is_triggered(value, bias)
