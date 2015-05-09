from db_comm import My_db_class

import Global
from Users import Users
import Trigger
import Reminder
import Symbol

class Report():
  report = []
  def __init__(self, list_of_names):
    """
    NOTE :
      - go through all triggered reminders and fetch a line
        of text from each; append to report
    """
    for name in list_of_names:
      for rem in Global.globe.users.get_by_name(name).check_reminders():
        self.report.append(rem.get_report_line())
    return None

  def __str__(self):
    return 'Generated Report :\n{report}'.format(report=self.report)

def init():
  """
  NOTE :  initialize database
  """
  Global.globe = Global.Global()

  Global.globe.db_obj  = My_db_class(Global.globe.db_filename)
  Global.globe.db      = Global.globe.db_obj.get_db()

  Global.globe.temp_db_obj = My_db_class(Global.globe.temp_db_loc)
  Global.globe.temp_db     = Global.globe.temp_db_obj.get_db()

  # initialize Users
  Global.globe.users   = Users()

def make_test_data():
  # add a user
  Global.globe.users.add_user('hari')

  # create a symbol
  Symbol.Symbol(name='RELIANCE.NS',y_symbol='RELIANCE.NS')

  # create a trigger
  trig1 = Trigger.Trigger(
      'RELIANCE.NS', 'RSI_period_1_param_10', '50', '+'
    )

  trig2 = Trigger.Trigger(
      'RELIANCE.NS', 'RSI_period_1_param_14', '50', '+'
    )
  trig3 = Trigger.Trigger(
      'RELIANCE.NS', 'RSI_period_1_param_30', '50', '+'
    )

  # useing trigger, create a reminder
  reminder  = Reminder.Reminder([trig1, trig2, trig3])
  Global.globe.users.get_by_name('hari').add_reminder(reminder)

def globe_plotter(plot_data):
  """
  plot_data is a list of lists; elements in
  each list is a tuple of a date and a floating
  value;
  For now, imagine that the y-axis range of all
  the lists are 0-100; TODO : we will have to
  merge plots such as price and RSI in the
  same graph
  """
  import matplotlib.pyplot as plt

  colors = ['r', 'b', 'g']

  x_axis_list = []
  y_axis_list = []

  for i in xrange(len(plot_data)):
    lst = plot_data[i]
    x_axis  = []
    y_axis  = []
    for y,x in lst:
      x_axis.append(x)
      y_axis.append(y)
    x_axis_list.append(x_axis)
    y_axis_list.append(y_axis)

  for i in xrange(len(x_axis_list)):
    plt.plot(x_axis_list[i], y_axis_list[i], colors[i])

  plt.ylabel('Attribute')
  plt.xlabel('Date')
  plt.show()

  return None

# this is the entry point
if __name__ == "__main__":
  init()

  make_test_data()

  list_of_names_to_fetch_reports_for = [
      'hari',
    ]
  print Report(list_of_names_to_fetch_reports_for)

  # plot from Global.globe.things_to_plot
  globe_plotter(Global.globe.things_to_plot)

  # after everything is done
  Global.globe.db_obj.close_db()
