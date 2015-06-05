import json

from django.db import models
from django import forms

from monitor.models.Symbol import Symbol
from monitor.models.Reminder import Reminder
from monitor.attribute import Attribute

class Trigger(models.Model):
  reminder  = models.ForeignKey(Reminder)
  symbol    = models.ForeignKey(Symbol)
  attrib    = models.CharField(max_length=200)
  trig_val  = models.CharField(max_length=30)
  bias      = models.CharField(max_length=30)

  def __unicode__(self):
    return '{symbol} {attrib} {trig_val} {bias}'.format(
        symbol=self.symbol, attrib=self.attrib,
        trig_val=self.trig_val, bias=self.bias,
      )

  def to_dict(self):
    attribs = self.attrib
    attribd = json.loads(attribs)
    trig_dict                  = {}
    trig_dict['attrib_name']   = attribd.get('root_name')
    trig_dict['attrib_options']= attribd.get('options')
    trig_dict['trig_val']      = self.trig_val
    trig_dict['bias']          = self.bias
    return trig_dict

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

  @staticmethod
  def is_reminder_triggered(reminder):
    triggered = True
    for trigger in Trigger.objects.filter(reminder=reminder):
      if trigger.is_triggered() == False:
        triggered = False
        break
    return triggered
    
