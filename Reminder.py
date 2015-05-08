class Reminder():
  """
  NOTE :
   - A reminder can contain a list of triggers
   - A trigger will contain a symbol, an attribute and a bias
   - A reminder is called triggered when all the triggers it
    contains are triggered / positive
  """
  trigger_list   = []

  def __init__(self, trigger_list=[]):
    self.trigger_list = trigger_list
    return None

  def add(self, trigger):
    self.trigger_list.append(trigger)
    return True

  def is_triggered(self):
    for t in self.trigger_list:
      if t.is_triggered() is False:
        return False
    return True

  def get_report_line(self):
    report_line = []
    for t in self.trigger_list:
      report_line.append(t.get_report_line())
    return report_line
