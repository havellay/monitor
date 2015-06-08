from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from stockman.settings import BASE_DIR

from monitor.market_times import open_time, close_time
from monitor.models.Config import Config
from monitor.models.Symbol import Symbol
from monitor.models.EoD import EoD
from monitor.models.Intraday import Intraday


class Command(BaseCommand):
  @staticmethod
  def custom_config_update_or_create(subject=None, predicate=None):
    return Config.objects.update_or_create(
        subject=subject,
        defaults={'subject':subject, 'predicate':predicate},
      )

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

    housekeeping_last_start_config_subject  = 'house_keeping_last_start'

    housekeeping_last_stop_config_subject   = 'house_keeping_last_stop'

    try:
      last_start,_ = Command.custom_config_update_or_create(
          subject=housekeeping_last_start_config_subject,
          predicate=datetime.now(),
        )
    except Exception as e:
      print 'something wrong happened when registering start time'
      print e

    last_action = Config.objects.filter(
        subject=housekeeping_last_action_config_subject,
      ).first()

    if datetime.now() < open_time or datetime.now() > close_time:
      print 'Market is closed'
      if last_action and last_action.predicate  == EoD_update_config_predicate:
        print 'Nothing to do'
      else:
        print 'perform EoD updates'
        try:
          last_action,_ = Command.custom_config_update_or_create(
              subject=housekeeping_last_action_config_subject,
              predicate=EoD_update_config_predicate,
            )
          EoD_updates()
        except Exception as e:
          print 'error when performing EoD_updates'
          print e
    else:
      print 'Market is open'
      print 'perform Intraday updates'
      try:
        last_action,_ = Command.custom_config_update_or_create(
            subject=housekeeping_last_action_config_subject,
            predicate=Intraday_update_config_predicate,
          )
        intraday_updates()
      except Exception as e:
        print 'error when performing intraday updates'
        print e

    last_stop,_ = Command.custom_config_update_or_create(
        subject=housekeeping_last_stop_config_subject,
        predicate=datetime.now(),
      )

    return None

def EoD_updates():
  for sym in Symbol.objects.all():
    EoD.append_latest(sym)
  return None

def intraday_updates():
  for sym in Symbol.objects.all():
    Intraday.append_latest(sym)
  return None


