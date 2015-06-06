from django.db import models

class Config(models.Model):
  subject   = models.CharField(primary_key=True, max_length=50)
  predicate = models.CharField(max_length=50, blank=True, null=True)

  def __unicode__(self):
    return '{subject} {predicate}'.format(
        subject=self.subject, predicate=self.predicate,
      )
