import datetime
import time

from db_comm import My_db_class

from Trigger import Trigger
from Reminder import Reminder
from Symbol import Symbol
from Report import Report
from Plotter import Plotter
from Users import Users

def init():
  """
  NOTE :  initialize database
  """
  My_db_class()

  # initialize Users
  Users()

def make_test_data():
  #### ADDING USER AND TRIGGERS FOR EoD
  Users.add_user('hari')
  # create a symbol
  reliance  = Symbol(name='Reliance',y_symbol='RELIANCE.BO',g_symbol='NSE:RELIANCE')
  # create a trigger
  trigger_list  = []
  trigger_list.append(
      Trigger(
          # s_symbol='RELIANCE.BO',
          symbol_obj=reliance,
          s_attribute='RSI_period_1_param_10',
          s_value='10',
          s_bias='+',
        )
    )
  trigger_list.append(
      Trigger(
          symbol_obj=reliance,
          s_attribute='RSI_period_1_param_20',
          s_value='10',
          s_bias='+',
        )
    )
  trigger_list.append(
      Trigger(
          symbol_obj=reliance,
          s_attribute='Price_',
          s_value='10',
          s_bias='+',
        )
    )
  # useing trigger, create a reminder
  reminder  = Reminder(trigger_list)
  Users.get_by_name('hari').add_reminder(reminder)

  #### ADDING USER AND TRIGGERS FOR intraday
  Users.add_user('hari_intraday')
  # create a symbol
  asianpaint  = Symbol(name='Asianpaint', y_symbol='ASIANPAINT.BO', g_symbol='NSE:ASIANPAINT')
  # create a trigger
  trigger_list  = []
  trigger_list.append(
      Trigger(
          symbol_obj=asianpaint,
          s_attribute='RSI_period_1_param_10_symbolmode_intraday',
          s_value='10',
          s_bias='+',
        )
    )
  trigger_list.append(
      Trigger(
          symbol_obj=asianpaint,
          s_attribute='RSI_period_1_param_20_symbolmode_intraday',
          s_value='10',
          s_bias='+',
        )
    )
  trigger_list.append(
      Trigger(
          symbol_obj=asianpaint,
          s_attribute='Price_symbolmode_intraday',
          s_value='10',
          s_bias='+',
        )
    )
  # useing trigger, create a reminder
  reminder  = Reminder(trigger_list)
  Users.get_by_name('hari_intraday').add_reminder(reminder)

# this is the entry point
if __name__ == "__main__":
  init()

  make_test_data()

  list_of_names_to_fetch_intraday_reports_for = [
      'hari_intraday',
    ]
  list_of_names_to_fetch_EoD_reports_for = [
      'hari',
    ]

  today2pm  = datetime.datetime.now().replace(
      hour=14, minute=0,
      second=0, microsecond=0
    )

  # while datetime.datetime.now() < today2pm:
  while True:
    time.sleep(1)                  # sleep for 15 seconds
    print 'woke up at : {}'.format(time.ctime())
    print Report(list_of_names_to_fetch_intraday_reports_for)
    print 'sleeping at : {}'.format(time.ctime())

  # update the End-of-Day prices with intraday
  # wipe away intraday prices

  print Report(list_of_names_to_fetch_EoD_reports_for)

  Plotter.globe_plotter(Plotter.get_plot_buffer())

  # after everything is done
  My_db_class.close_db()
