from django.db import models

from .User import User

class Reminder(models.Model):
  user  = models.ForeignKey(User)

  def __unicode__(self):
    return '{user}'.format(user=self.user)

  @staticmethod
  def append_new(user=None):
    reminder  = Reminder(user=user)
    reminder.save()
    return reminder
