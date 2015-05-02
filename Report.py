from db_comm import My_db_class
import Users

# Globals
db_obj  = None
db      = None
users   = None

class Report():
  report = []
  def __init__(self, name):
    """
    TODO : Maybe a single report should be for multiple users
    """
    """
    NOTE :
      - go through all triggered reminders and fetch a line
        of text from each; append to report
    """
    for rem in users.get_by_name(name).check_reminders():
      self.report.append(rem.get_report_line())
    return self.report

  def __str__(self):
    return 'Generated Report :\n{report}'.format(report=self.report)

def init():
  """
  NOTE :  initialize database
  """
  global db_obj, db, users

  db_obj  = My_db_class()
  db      = My_db_class.get_db()

  # initialize Users
  users   = Users()

# this is the entry point
if __name__ == "__main__":
  init()

  print Report('hari')

  # after everything is done
  db_obj.close_db()
