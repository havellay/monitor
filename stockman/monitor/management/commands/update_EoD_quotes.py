"""
  This command will fetch the EoD prices
  all symbols we care about and update the database
"""

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
  def handle(self, *args, **options):
    return None
