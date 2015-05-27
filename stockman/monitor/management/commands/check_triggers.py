from django.core.management.base import BaseCommand, CommandError

from monitor.models.Trigger import Trigger

"""
  This command will fetch the current live prices of
  all symbols we care about and update the database
"""

class Command(BaseCommand):
  def handle(self, *args, **options):
    for t in Trigger.objects.all():
      print t.is_triggered()
    return None
