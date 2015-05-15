import datetime
import time

from db_comm import My_db_class

import Global
import Trigger
import Reminder
import Symbol
from Report import Report
from plotter import globe_plotter
from Users import Users

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
  trigger_list  = [
      Trigger.Trigger(
          'RELIANCE.NS', 'RSI_period_1_param_10', '10', '+'
        )
    ]
  trigger_list.append(
      Trigger.Trigger(
          'RELIANCE.NS', 'RSI_period_1_param_20', '10', '+'
        )
    )
  trigger_list.append(
      Trigger.Trigger(
          'RELIANCE.NS', 'Price_', '10', '+'
        )
    )

  # useing trigger, create a reminder
  reminder  = Reminder.Reminder(trigger_list)
  Global.globe.users.get_by_name('hari').add_reminder(reminder)

# this is the entry point
if __name__ == "__main__":
  init()

  make_test_data()

  list_of_names_to_fetch_intraday_reports_for = [
      # 'hari_intraday',
    ]
  list_of_names_to_fetch_EoD_reports_for = [
      'hari',
    ]

  today2pm  = datetime.datetime.now().replace(
      hour=14, minute=0,
      second=0, microsecond=0
    )

  while datetime.datetime.now() < today2pm:
    time.sleep(15)                  # sleep for 15 seconds
    print 'woke up at : {}'.format(time.ctime())
    print Report(list_of_names_to_fetch_intraday_reports_for)
    print 'sleeping at : {}'.format(time.ctime())

  # update the End-of-Day prices with intraday
  # wipe away intraday prices

  print Report(list_of_names_to_fetch_EoD_reports_for)

  # plot from Global.globe.things_to_plot
  globe_plotter(Global.globe.things_to_plot)

  # after everything is done
  Global.globe.db_obj.close_db()
