from django.db import models
from django import forms

from .Symbol import Symbol
from .Reminder import Reminder
from monitor.attribute import Attribute

class Trigger(models.Model):
  reminder  = models.ForeignKey(Reminder)
  symbol    = models.ForeignKey(Symbol)
  attrib    = models.CharField(max_length=100)
  trig_val  = models.CharField(max_length=30)
  bias      = models.CharField(max_length=30)

  def is_triggered(self):
    return Attribute.is_triggered(self)

  @staticmethod
  def append_new(
      reminder=None, symbol=None, attrib=None,
      trig_val=None, bias=None,
    ):
    trigger = Trigger(
        reminder=reminder, symbol=symbol, attrib=attrib,
        trig_val=trig_val, bias=bias,
      )
    trigger.save()
    return True


