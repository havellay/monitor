from django.db import models

from monitor.picker import Picker

from .Symbol import Symbol

class Intraday(models.Model):
  symbol  = models.ForeignKey(Symbol)
  time    = models.DateTimeField(auto_now=True) # not sure whether this
                                                # should be true
  quote   = models.DecimalField(max_digits=9, decimal_places=2)
  volume  = models.IntegerField()

  def __unicode__(self):
    return '{symbol} for {quote} at {time}'.format(
        symbol=self.symbol, quote=self.quote, time=self.time,
      )

  @staticmethod
  def append_latest_price(symbol):
    intraday_quote  = Intraday()
    price,volume    = Picker.get_current_price_volume(symbol)
    intraday_quote.symbol = symbol
    intraday_quote.quote  = price
    intraday_quote.volume = volume
    intraday_quote.save()
