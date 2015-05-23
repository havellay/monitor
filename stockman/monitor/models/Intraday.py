from django.db import models

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
