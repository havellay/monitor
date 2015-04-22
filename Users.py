class User():
    uid         = 0
    name        = ''
    reminders   = []
    email       = ''

    def __init__(self, uid, name):
        self.uid    = uid
        self.name   = name
        return True

    def update_email(self, email):
        self.email  = email
        return True

    def add_reminder(self, reminder):
        self.reminders.append(reminder)
        return True

class Users():
    user_list = []

    def add_user(self, name):
        nu = User(len(user_list), name)
        user_list.append(nu)
        return nu

    def get_user(self, uid):
        # Exception : uid could be an invalid index
        return user_list[uid]
