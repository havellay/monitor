from datetime import datetime
# all times are in UTC
# set these variables in the database? These are config values;
# find out what the right way of storing configs is.
# well, technically, the configs in the database aren't configs
# they are more like status

close_time  = datetime.now().replace(
    hour=10, minute=30, second=0, microsecond=0,
  )
open_time   = datetime.now().replace(
    hour=3, minute=30, second=0, microsecond=0,
  )
