from stockman.settings import BASE_DIR

from django.core.management.base import BaseCommand, CommandError

from monitor.models.Symbol import Symbol

class Command(BaseCommand):
  def handle(self, *args, **options):
    print BASE_DIR

    from monitor.models.Symbol import Symbol
    from yahoo_finance import Share
    
    for sym in Symbol.objects.all():
      done = False
      while not done:
        try:
          print '{symbol} as {obj}'.format(
              symbol=sym.y_symbol,
              obj=Share(sym.y_symbol)
            )
          done = True
        except Exception as e:
          print 'for {symbol} exception {e}'.format(symbol=sym.y_symbol, e=e)
          continue
