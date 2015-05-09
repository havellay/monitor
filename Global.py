import Attribute

globe = None

class Global():
  attrib_dict = {} 
  db_obj       = None
  db           = None
  db_filename  = 'data/db'
  temp_db_obj  = None
  temp_db      = None
  temp_db_loc  = ':memory:'
  users        = None
  things_to_plot = []

  def __init__(self):
    self.attrib_dict['RSI'] = Attribute.RSI
    return None
