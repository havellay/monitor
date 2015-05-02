class Reminder():
  """
  NOTE :
   - A reminder can contain a list of triggers
   - A trigger will contain a symbol, an attribute and a bias
   - A reminder is called triggered when all the triggers it
    contains are triggered / positive
  """
  self.trigger_list   = []

  def __init__(self, trigger_list=[]):
    self.trigger_list = trigger_list
    return True

  def add(self, trigger):
    self.trigger_list.append(trigger)
    return True

  def is_triggered(self):
    ret = True
    for t in self.trigger_list:
      ret = ret and t.is_triggered()
    return ret
