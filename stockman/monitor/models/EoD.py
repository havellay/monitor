from django.db import models
from datetime import date, datetime

from .Symbol import Symbol
from monitor.picker import Picker
from monitor.market_times  import close_time

class EoD(models.Model):
  symbol    = models.ForeignKey(Symbol)
  date      = models.DateTimeField(auto_now=True) # not sure whether this
                                                  # should be true
  open_qt   = models.DecimalField(max_digits=9, decimal_places=2)
  close_qt  = models.DecimalField(max_digits=9, decimal_places=2)
  high_qt   = models.DecimalField(max_digits=9, decimal_places=2)
  low_qt    = models.DecimalField(max_digits=9, decimal_places=2)
  volume    = models.IntegerField()

  def __unicode__(self):
    return '{symbol} for {close} at {date}'.format(
        symbol=self.symbol, close=self.close_qt, date=self.date,
      )

  @staticmethod
  def append_latest(sym):
    if datetime.now() < close_time:
      return None
    current_quotes  = EoD.objects.filter(symbol=sym)
    if not current_quotes:
      # Symbol is being processed first time; fetch all
      # quotes from May 1st 2014
      from_date = datetime.strptime('2014-05-01', '%Y-%m-%d').date()
      dict_list = Picker.get_historical(sym, from_date, date.today())
      for x in dict_list:
        eod = EoD(
            symbol=sym, open_qt=x.get('open_qt'), close_qt=x.get('close_qt'),
            high_qt=x.get('high_qt'), low_qt=x.get('low_qt'),
            volume=x.get('volume'),
          )
        eod.save()
    else:
      # There are some quotes for this symbol already;
      # assume that these are quotes from May 1st 2014
      # onwards and fetch the last close price
      ld  = Picker.get_current(sym)
      eod = EoD(
          symbol=sym, open_qt=ld.get('open'), close_qt=ld.get('close'),
          high_qt=ld.get('high'), low_qt=ld.get('low'),
          volume=ld.get('volume'),
        )
      eod.save()
    return None

