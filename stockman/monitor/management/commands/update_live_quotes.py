from django.core.management.base import BaseCommand, CommandError

from monitor.models import Symbol, Intraday

"""
  This command will fetch the current live prices of
  all symbols we care about and update the database
"""

class Command(BaseCommand):
  def handle(self, *args, **options):
    for sym in Symbol.Symbol.objects.all():
      Intraday.Intraday.append_latest_price(sym)
    return None
