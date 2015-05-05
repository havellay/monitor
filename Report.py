from db_comm import My_db_class
from Users import Users

# Globals
db_obj      = None
db          = None
db_filename = 'data/db'
temp_db_obj = None
temp_db     = None
temp_db_loc = ':memory:'
users       = None

class Report():
  report = []
  def __init__(self, list_of_names):
    """
    NOTE :
      - go through all triggered reminders and fetch a line
        of text from each; append to report
    """
    for name in list_of_names:
      for rem in users.get_by_name(name).check_reminders():
        self.report.append(rem.get_report_line())
    return None

  def __str__(self):
    return 'Generated Report :\n{report}'.format(report=self.report)

def init():
  """
  NOTE :  initialize database
  """
  global db_obj, db, users, db_filename
  global temp_db_obj, temp_db, temp_db_loc

  db_obj  = My_db_class(db_filename)
  db      = db_obj.get_db()

  temp_db_obj = My_db_class(temp_db_loc)
  temp_db     = temp_db_obj.get_db()

  # initialize Users
  users   = Users()
  """
  TODO : Add some information here; need to add users etc.
  """

def make_test_data():
  # add a user
  users.add_user('hari')

  # create a trigger

  # useing trigger, create a reminder

# this is the entry point
if __name__ == "__main__":
  init()

  make_test_data()

  list_of_names = [
      'hari',
    ]
  print Report(list_of_names)

  # after everything is done
  db_obj.close_db()
