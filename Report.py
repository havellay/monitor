import Global

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

