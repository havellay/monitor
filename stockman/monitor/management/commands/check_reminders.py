from django.core.management.base import BaseCommand, CommandError

from monitor.models.Trigger import Trigger
from monitor.models.Reminder import Reminder

"""
  This command will fetch the current live prices of
  all symbols we care about and update the database
"""

class Command(BaseCommand):
  def handle(self, *args, **options):
    for r in Reminder.objects.all():
      print r.check_is_triggered()
    return None
