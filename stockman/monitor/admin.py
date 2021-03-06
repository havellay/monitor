from django.contrib import admin

# TODO find a better way to do the following :
#   like from models import ....

from models.Symbol import Symbol
from models.EoD import EoD
from models.Intraday import Intraday
from models.User import User
from models.Reminder import Reminder
from models.Trigger import Trigger
from models.Config import Config

class SymbolAdmin(admin.ModelAdmin):
  list_display  = ('name', 'y_symbol', 'g_symbol', 'nse_symbol')
  search_fields = ('name', 'y_symbol', 'g_symbol', 'nse_symbol')

admin.site.register(Symbol, SymbolAdmin)
admin.site.register(EoD)
admin.site.register(Intraday)
admin.site.register(User)
admin.site.register(Reminder)
admin.site.register(Trigger)
admin.site.register(Config)

# Register your models here.
