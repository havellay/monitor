class Report():
    # every instance of this class is associated with either one or more
    # users. when a report is generated, specific triggers of specific
    # users are checked
    def __init__(self, user_name):
        return True

    def for_user(self, user):
        return None

db_obj  = None
db      = None

# this is the entry point
if __name__ == "__main__":
    # initialize database
    global db_obj
    global db
    db_obj  = My_db_class()
    db      = My_db_class.get_db()

    report = Report('hari')

    # after everything is done
    db_obj.close_db()
