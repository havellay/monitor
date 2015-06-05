from datetime import datetime
# all times are in UTC

close_time  = datetime.now().replace(
    hour=10, minute=30, second=0, microsecond=0,
  )
open_time   = datetime.now().replace(
    hour=3, minute=30, second=0, microsecond=0,
  )
