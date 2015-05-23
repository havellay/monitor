from django.db import models

class Symbol(models.Model):
  name      = models.CharField(max_length=30)
  y_symbol  = models.CharField(max_length=30, blank=True, verbose_name='Yahoo Symbol')
  g_symbol  = models.CharField(max_length=30, blank=True, verbose_name='Google Symbol')

  def __unicode__(self):
    return self.name

  class Meta:
    ordering  = ['name']

