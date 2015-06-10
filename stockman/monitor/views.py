import datetime
import json

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Template, Context
from django.shortcuts import render

from stockman.settings import BASE_DIR

from monitor.forms import SymbolForm, TriggerForm
from monitor.attribute import Attribute
from monitor.models.Symbol import Symbol
from monitor.models.Reminder import Reminder
from monitor.models.Trigger import Trigger
from monitor.models.User import User

# Create your views here.

def get_index(request):
  try:
    fp = open(BASE_DIR+'/templates/monitor/index.html','r')
    content = fp.read()
  except Exception:
    print 'problem reading index.html'
  return HttpResponse(content)


def insert_symbol(request):
  if request.method == 'POST':
    form  = SymbolForm(request.POST)
    if form.is_valid():
      cd  = form.cleaned_data
      Symbol.append_new(
          name=cd.get('name'), y_symbol=cd.get('y_symbol'),
          g_symbol=cd.get('g_symbol'), nse_symbol=cd.get('nse_symbol'),
        )
  else:
    form  = SymbolForm()
  return render(
      request, 'monitor/insert_symbol.html', {'form':form},
    )


def insert_reminder(request):
  if request.method == 'POST':
    optd    = {}
    invalid = '---'
    form    = TriggerForm(request.POST)
    # {
    #   'attribute2': u'---',
    #   'attribute1_hidden': u'{"time_unit":"day","time_param":"10","bias":"+"}',
    #   'symbol': u'ONGC', 'attribute1': u'self', 'attribute2_hidden': u''
    # }
    if form.is_valid():
      cd      = form.cleaned_data
      user    = User.objects.filter(login='hari')[0]
      symbol  = Symbol.objects.filter(name=cd.get('symbol'))[0]
      attribute_dicts = []
      for x in cd:
        if 'attribute' in x and 'hidden' not in x and cd.get(x) != invalid:
          try:
            optd            = json.loads(cd.get(x+'_hidden'))
          except Exception:
            print 'malformed option string'
          # optd['symbol']    = symbol.name
          optd['attribute'] = cd.get(x)
          optd['symbol_id'] = symbol.id
          optd['user']      = user.login  # hard-coding this now, have to change
          c_optd  = Attribute.to_clean_optd(optd)
          if c_optd:
            attribute_dicts.append(c_optd)
      reminder  = Reminder.append_new(user=user)
      attrib    = Attribute.optd_to_file_name(c_optd)
      for x in attribute_dicts:
        import ipdb; ipdb.set_trace()
        Trigger.append_new(
            reminder=reminder, symbol=symbol, attrib=attrib,
            trig_val=c_optd.get('trig_val'), bias=c_optd.get('bias'),
          )
  else:
    form  = TriggerForm()
  return render(
      request, 'monitor/insert_reminder.html', {'form':form},
    )


def get_attrib_form(request):
  form = None
  if request.GET.get('attrib'):
    form = Attribute.get_form(request.GET['attrib'])
  t = Template('{{ form }}')
  html = t.render(Context({'form':form}))
  return HttpResponse(html)


def get_triggered_reminders(request):
  # make some changes here to make sure that we spew out
  # proper html instead of just dicts; it may be easier
  # to do html based things here
  # rl = Reminder.triggered_reminders()
  rl = Reminder.objects.filter(is_triggered=True)
  rdl = [] # reminder dict list
  for r in rl:
    rdl.append(r.to_dict())
  return render(
      request,
      'monitor/get_triggered_reminders.html',
      {
        'rdl':rdl,
      },
    )


def provide_script(request, dname=None, fname=None):
  """
  This method can be dangerous and can be used
  to fetch files; think of a better solution
  """
  try:
    import mimetypes
    full_path   = BASE_DIR+'/templates/monitor/'+dname+'/'+fname
    fp          = open(full_path, 'r')
    content     = fp.read()
    content_type,_ = mimetypes.guess_type(full_path)
  except Exception as e:
    print 'problem reading script'
    print e
  return HttpResponse(content, content_type=content_type)


# get rid of functions below this comment

def print_request_info(request):
  request_meta_list = []
  for x in request.META:
    request_meta_list.append((x, request.META[x]))
  return render(
      request,
      'monitor/print_request_info.html',
      {
        'request_path':request.path,
        'request_host':request.get_host(),
        'request_full_path':request.get_full_path(),
        'request_is_secure':request.is_secure(),
        'request_meta_list':request_meta_list,
      },
    )

def scratch(request):
  return render(request, 'monitor/scratch/index.html', {})

def get_form(request):
  return render(request, 'monitor/scratch/form.html', {})
