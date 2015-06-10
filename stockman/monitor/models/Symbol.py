from django.db import models

class Symbol(models.Model):
  name        = models.CharField(max_length=30, unique=True)
  y_symbol    = models.CharField(
      max_length=30, blank=True, verbose_name='Yahoo Symbol', unique=True,
    )
  g_symbol    = models.CharField(
      max_length=30, blank=True, verbose_name='Google Symbol', # unique=True,
    )
  nse_symbol  = models.CharField(
      max_length=30, blank=True, verbose_name='NSE India Symbol', unique=True,
    )

  def __unicode__(self):
    return self.name

  @staticmethod
  def append_new(
      name=None, y_symbol=None, g_symbol=None, nse_symbol=None,
    ):
    sym = Symbol(
        name=name, y_symbol=y_symbol, g_symbol=g_symbol, nse_symbol=nse_symbol,
      )
    sym.save()

  class Meta:
    ordering  = ['name']
