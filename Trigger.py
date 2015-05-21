from Symbol import Symbol

class Trigger(object):
  """
  NOTE :
   - `symbol`, `attribute`, `value` and `bias` are all strings
   - Symbol_dict.get(symbol).get_attrib(attribute).is_triggered(value, bias)
    the above is the ideal call;
  """
  def __init__(self,
      s_symbol=None,
      s_attribute=None,
      s_value=None,
      s_bias=None,
      symbol_obj=None,
    ):
    self.s_symbol       = s_symbol
    self.symbol_obj     = symbol_obj
    self.s_attribute    = s_attribute
    self.s_value        = s_value
    self.s_bias         = s_bias
    self.f_current_val  = None

    if not symbol_obj and s_symbol:
      self.symbol_obj = Symbol.get_from_symbol_dict(s_symbol)
    return None

  def __str__(self):
    return '{0} {1} {2} {3} {4}'.format(
        self.s_symbol, self.s_attribute,
        self.s_value, self.s_bias,
        self.f_current_val
      )

  def is_triggered(self):
    flag, self.f_current_val = self.symbol_obj.get_attrib(
          s_attrib=self.s_attribute,
        ).is_triggered(
            self.s_value,
            self.s_bias
          )
    return flag

  def get_report_line(self):
    return self.__str__()
