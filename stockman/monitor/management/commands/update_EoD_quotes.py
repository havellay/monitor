from django.core.management.base import BaseCommand, CommandError

from monitor.models import Symbol, EoD

"""
  This command will fetch the EoD prices
  all symbols we care about and update the database
"""

class Command(BaseCommand):
  def handle(self, *args, **options):
    for sym in Symbol.Symbol.objects.all():
      EoD.EoD.append_latest(sym)
    return None
