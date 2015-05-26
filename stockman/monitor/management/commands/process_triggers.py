"""
  This command will :
    - go through all reminders of all users and find whether they 
      have been triggered
"""

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
  def handle(self, *args, **options):
    print 'hello'
    return None
