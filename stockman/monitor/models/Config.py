from django.db import models

class Config(models.Model):
  subject   = models.CharField(primary_key=True, max_length=50)
  predicate = models.CharField(max_length=50, blank=True, null=True)

  def __unicode__(self):
    return '{subject} {predicate}'.format(
        subject=self.subject, predicate=self.predicate,
      )

  @staticmethod
  def set(subject=None, predicate=None):
    if not subject:
      return False
    config    = Config.objects.filter(subject=subject).first()
    if config:
      config.predicate  = predicate
    else:
      config  = Config(subject=subject, predicate=predicate)
    config.save()
    return predicate
