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

def xy_tuple_to_lists(lst_of_tuples):
  x_list  = []
  y_list  = []
  max_y   = float('-inf')
  min_y   = float('inf')
  for y,x in lst_of_tuples:
    max_y = max_y if max_y > y else y
    min_y = min_y if min_y < y else y
    x_list.append(x)
    y_list.append(y)
  return x_list, y_list, max_y, min_y

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
  from mpl_toolkits.axes_grid1 import host_subplot
  import mpl_toolkits.axisartist as AA
  import matplotlib.pyplot as plt

  y_limit_raw = []

  host  = host_subplot(111, axes_class=AA.Axes)
  # plt.subplots_adjust(right=0.55)

  host.set_xlabel('Date')             # strong assumption
  host.set_ylabel(plot_data[0][0])    # name of the first plot

  host_x_list, host_y_list, max_y, min_y = xy_tuple_to_lists(plot_data[0][1])
  y_limit_raw.append(
      [
        plot_data[0][0][:plot_data[0][0].index('_')],
        max_y, min_y, host
      ]
    )

  p1, = host.plot(host_x_list, host_y_list, label=plot_data[0][0])
  host.axis['left'].label.set_color(p1.get_color())

  if len(plot_data) > 1:
    offset      = 60
    for i in xrange(len(plot_data)-1):
      par = host.twinx()
      new_fixed_axis    = par.get_grid_helper().new_fixed_axis
      par.axis['right'] = new_fixed_axis(loc='right',
                                          axes=par,
                                          offset=(offset*i,0))
      par.axis['right'].toggle(all=True)
      par.set_ylabel(plot_data[i+1][0])

      par_x_list, par_y_list, max_y, min_y  = xy_tuple_to_lists(
          plot_data[i+1][1]
        )
      y_limit_raw.append(
          [
            plot_data[i+1][0][:plot_data[i+1][0].index('_')],
            max_y, min_y, par
          ]
        )

      p, = par.plot(par_x_list, par_y_list, label=plot_data[i+1][0])
      par.axis['right'].label.set_color(p.get_color())

  # find limits of the y axis
  for i in xrange(len(y_limit_raw)-1):
    for j in xrange(i+1, len(y_limit_raw)):
      if y_limit_raw[i][0] == y_limit_raw[j][0]:
        i_max = y_limit_raw[i][1]; j_max  = y_limit_raw[j][1]
        i_min = y_limit_raw[i][2]; j_min  = y_limit_raw[j][2]
        y_limit_raw[i][1] = y_limit_raw[j][1] = max(i_max, j_max)
        y_limit_raw[i][2] = y_limit_raw[j][2] = min(i_min, j_min)

  for x,max_y,min_y,par in y_limit_raw:
    par.set_ylim(min_y, max_y)
  
  host.legend()
  host.grid()
  plt.draw()
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
