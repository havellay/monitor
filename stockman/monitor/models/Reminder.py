from django.db import models

from monitor.models.User import User

class Reminder(models.Model):
  user          = models.ForeignKey(User)
  is_triggered  = models.BooleanField(default=False)
  # have symbol as a field of reminder ??

  def check_is_triggered(self):
    from monitor.models.Trigger import Trigger
    triggers = Trigger.objects.filter(reminder=self)
    self.is_triggered = True
    for t in triggers:
      if not t.check_is_triggered():
        self.is_triggered = False
        break
    self.save()
    return self.is_triggered

  def to_dict(self):
    from monitor.models.Trigger import Trigger

    rem_dict  = {}
    triggers  = Trigger.objects.filter(reminder=self)
    count     = 1

    for t in triggers:
      if not rem_dict.get('symbol'):
        rem_dict['symbol'] = str(t.symbol)
      trig_str = 'trigger'+str(count)
      rem_dict[trig_str] = t.to_dict()
      count += 1

    return rem_dict

  def __unicode__(self):
    from monitor.models.Trigger import Trigger
    string    = ''
    triggers  = Trigger.objects.filter(reminder=self)
    for t in triggers:
      string  = string + t.__unicode__()
    return string

  @staticmethod
  def append_new(user=None):
    reminder  = Reminder(user=user)
    reminder.save()
    return reminder

  @staticmethod
  def triggered_reminders():
    # the following import statement is here to cure
    # a circular dependency problem; TODO think of a 
    # better solution to this
    from monitor.models.Trigger import Trigger

    triggered_reminders = []

    for rem in Reminder.objects.all():
      if Trigger.is_reminder_triggered(rem):
        triggered_reminders.append(rem)

    return triggered_reminders
