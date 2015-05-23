from django.db import models

from .User import User

class Reminder(models.Model):
  user  = models.ForeignKey(User)
