class User(object):
  def __init__(self, uid, name):
    self.uid        = uid
    self.name       = name
    self.reminders  = []
    self.email      = ''
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


class Users(object):
  user_list = []
  user_dict = {}

  def __init__(self):
    return None

  @staticmethod
  def add_user(name):
    nu = User(len(Users.user_list), name)
    Users.user_list.append(nu)
    Users.user_dict[name] = nu
    return nu

  @staticmethod
  def get_by_uid(uid):
    """
    TODO : Exception : uid could be an invalid index
    """
    return Users.user_list[uid]

  @staticmethod
  def get_by_name(name):
    """
    TODO : Exception : user with `name` may not exist
    """
    return Users.user_dict.get(name)
