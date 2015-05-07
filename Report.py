import Global
from db_comm import My_db_class
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
  trigger   = Trigger.Trigger('RELIANCE.NS', 'RSI_period1_param_10', '10', '+')

  # useing trigger, create a reminder
  reminder  = Reminder.Reminder([trigger])
  Global.globe.users.get_by_name('hari').add_reminder(reminder)

# this is the entry point
if __name__ == "__main__":
  init()

  make_test_data()

  list_of_names_to_fetch_reports_for = [
      'hari',
    ]
  print Report(list_of_names_to_fetch_reports_for)

  # after everything is done
  Global.globe.db_obj.close_db()
