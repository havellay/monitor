from django.db import models

# Create your models here.
class Symbol(models.Model):
  name      = models.CharField(max_length=30)
  y_symbol  = models.CharField(max_length=30)
  g_symbol  = models.CharField(max_length=30)

  def __unicode__(self):
    return self.name

  class Meta:
    ordering  = ['name']

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

class User(models.Model):
  login     = models.CharField(max_length=30)
  password  = models.CharField(max_length=40) # How to store passwords
  username  = models.CharField(max_length=30)
  email     = models.EmailField()
  
  def __unicode__(self):
    return '{username} logs in with {login}; email address is {email}'.format(
        username=self.username, login=self.login, email=self.email,
      )
    pass

class Reminder(models.Model):
  user  = models.ForeignKey(User)

class Trigger(models.Model):
  reminder  = models.ForeignKey(Reminder)
  symbol    = models.ForeignKey(Symbol)
  attrib    = models.CharField(max_length=100)
  trig_val  = models.CharField(max_length=30)
  bias      = models.CharField(max_length=30)
