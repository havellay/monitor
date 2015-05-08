from Symbol import symbol_dict

class Trigger():
  """
  NOTE :
   - `symbol`, `attribute`, `value` and `bias` are all strings
   - Symbol_dict.get(symbol).get_attrib(attribute).is_triggered(value, bias)
    the above is the ideal call;
  """
  s_symbol     = ''
  s_attribute  = ''
  s_value      = ''
  s_bias       = ''
  f_current_val = 0

  def __init__(self, s_symbol, s_attribute, s_value, s_bias):
    self.s_symbol     = s_symbol
    self.s_attribute  = s_attribute
    self.s_value      = s_value
    self.s_bias       = s_bias
    return None

  def __str__(self):
    return '{0} {1} {2} {3} {4}'.format(
        self.s_symbol, self.s_attribute,
        self.s_value, self.s_bias, self.f_current_val
      )

  def is_triggered(self):
    # global symbol_dict --> this may not be needed
    flag, self.f_current_val = symbol_dict.get(self.s_symbol).get_attrib(
                  self.s_attribute).is_triggered(self.s_value, self.s_bias)
    return flag

  def get_report_line(self):
    return self.__str__()
