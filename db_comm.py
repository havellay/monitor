import sqlite3

class Queries():
  @staticmethod
  def s_filename_f_quotetab_w_symbol_eq(cursor, s_symbol):
    cursor.execute('SELECT filename from quotetab where symbol=?',[s_symbol])
    return cursor

  @staticmethod
  def i_filename_symbol_i_quotetab(cursor, filename, s_symbol):
    cursor.execute(
        'INSERT INTO quotetab (symbol, filename) VALUES (?, ?)',
        [s_symbol, filename]
      )

  @staticmethod
  def TMP_ct_SYMBOL_w_date_close(cursor, s_symbol):
    cursor.execute('CREATE TABLE ?(date DATE, close REAL)', [s_symbol])
    return cursor

class My_db_class():
  db        = None
  file_name = None

  def __init__(self, file_name):
    self.file_name  = file_name
    self.db         = sqlite3.connect(self.file_name)
    return None

  def get_db(self):
    return self.db

  def close_db(self):
    # this is obselete. Use the 'with' keyword.
# refer http://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
    return self.db.close()
