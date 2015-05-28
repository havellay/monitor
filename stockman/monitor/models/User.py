from django.db import models

class User(models.Model):
  login     = models.CharField(max_length=30)
  password  = models.CharField(max_length=40) # How to store passwords
  username  = models.CharField(max_length=30, blank=True)
  email     = models.EmailField(blank=True)
  
  def __unicode__(self):
    return '{username} logs in with {login}; email address is {email}'.format(
        username=self.username, login=self.login, email=self.email,
      )
