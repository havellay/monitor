from stockman.settings import BASE_DIR

from django.core.management.base import BaseCommand, CommandError

from monitor.models.Symbol import Symbol

class Command(BaseCommand):
  def handle(self, *args, **options):
    print BASE_DIR
    for x in Symbol.objects.all():
      print x.id
    return None
