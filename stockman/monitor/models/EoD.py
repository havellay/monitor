from django.db import models

from .Symbol import Symbol

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
        symbol=self.symbol, close=close_qt, date=date,
      )
