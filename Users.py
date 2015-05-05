class User():
  uid         = 0
  name        = ''
  reminders   = []
  email       = ''

  def __init__(self, uid, name):
    self.uid    = uid
    self.name   = name
    return None

  def update_email(self, email):
    self.email  = email
    return True

  def add_reminder(self, reminder):
    """
    TODO : There is no way that this is sufficient
    """
    self.reminders.append(reminder)
    return True

  def check_reminders(self):
    """
    NOTE : 
      - go through all the reminders
      - check whether any reminder has been triggered
      - make list of triggered reminders, return this
    """
    triggered = [
        reminder for reminder in self.reminders 
          if reminder.is_triggered() is True
      ]
    return triggered

class Users():
  user_list = []
  user_dict = {}

  def __init__(self):
    # Nothing to do
    return None

  def add_user(self, name):
    nu = User(len(self.user_list), name)
    self.user_list.append(nu)
    self.user_dict[name] = nu
    return nu

  def get_by_uid(self, uid):
    """
    TODO : Exception : uid could be an invalid index
    """
    return user_list[uid]

  def get_by_name(self, name):
    """
    TODO : Exception : user with `name` may not exist
    """
    return self.user_dict.get(name)
