from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

from monitor.forms import SymbolForm, TriggerForm

import datetime

# Create your views here.

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

def insert_symbol(request):
  if request.method == 'POST':
    form  = SymbolForm(request.POST)
    if form.is_valid():
      cd  = form.cleaned_data
      for x in cd:
        print cd.get(x)
  else:
    form  = SymbolForm()
  return render(
      request, 'monitor/insert_symbol.html', {'form':form},
    )

def insert_trigger(request):
  if request.method == 'POST':
    form  = TriggerForm(request.POST)
    if form.is_valid():
      cd  = form.cleaned_data
      for x in cd:
        print cd.get(x)
  else:
    import ipdb; ipdb.set_trace()
    form  = TriggerForm()
  return render(
      request, 'monitor/insert_trigger.html', {'form':form},
    )
