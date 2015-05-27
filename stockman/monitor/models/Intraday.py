from django.db import models

from monitor.picker import Picker

from .Symbol import Symbol

class Intraday(models.Model):
  symbol  = models.ForeignKey(Symbol)
  time    = models.DateTimeField()
  quote   = models.DecimalField(max_digits=9, decimal_places=2)
  volume  = models.IntegerField()

  def __unicode__(self):
    return '{symbol} for {quote} at {time}'.format(
        symbol=self.symbol, quote=self.quote, time=self.time,
      )

  @staticmethod
  def append_latest(symbol):
    # Maybe this method is responsible to ensure that frequent
    # additions to the database doesn't happen and instead
    # quotes are only added once in 2 minutes or something
    latest_dict     = Picker.get_current(symbol)
    intraday_quote  = Intraday(
        symbol=symbol, quote=latest_dict.get('quote'),
        volume=latest_dict.get('volume'),
        time=latest_dict.get('time'),
      )
    intraday_quote.save()
