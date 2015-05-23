from django.db import models

from .Symbol import Symbol
from .Reminder import Reminder

class Trigger(models.Model):
  reminder  = models.ForeignKey(Reminder)
  symbol    = models.ForeignKey(Symbol)
  attrib    = models.CharField(max_length=100)
  trig_val  = models.CharField(max_length=30)
  bias      = models.CharField(max_length=30)
