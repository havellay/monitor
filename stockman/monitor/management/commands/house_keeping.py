from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from stockman.settings import BASE_DIR

from monitor.market_times import open_time, close_time
from monitor.models.Config import Config
from monitor.models.Symbol import Symbol
from monitor.models.EoD import EoD
from monitor.models.Intraday import Intraday

class Command(BaseCommand):
  def handle(self, *args, **options):
    """
    It is expected that there will only be one thread
    running this method; I don't think the database
    operations done here are atomic because of how
    far the read, assigns and save() are from eachother
    """
    housekeeping_last_action_config_subject = 'house_keeping_last_action'
    EoD_update_config_predicate             = 'EoD_update'
    Intraday_update_config_predicate        = 'Intraday_update'

    last_action = Config.objects.filter(
        subject=housekeeping_last_action_config_subject
      ).first()

    if not last_action:
      last_action = Config.set(
          subject=housekeeping_last_action_config_subject,
          predicate=None
        )
      last_action.save()

    if datetime.now() < open_time or datetime.now() > close_time:
      print 'Market is closed'
      if last_action.predicate  == EoD_update_config_predicate:
        print 'Nothing to do'
        return None
      else:
        print 'perform EoD updates'
        last_action.predicate = EoD_update_config_predicate
        EoD_updates()
    else:
      print 'Market is open'
      print 'perform Intraday updates'
      last_action.predicate = Intraday_update_config_predicate
      intraday_updates()

    last_action.save()
    return None

def EoD_updates():
  for sym in Symbol.objects.all():
    EoD.append_latest(sym)
  return None

def intraday_updates():
  for sym in Symbol.objects.all():
    Intraday.append_latest(sym)
  return None
