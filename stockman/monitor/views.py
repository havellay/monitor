from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

import datetime

# Create your views here.

def hello(request):
  return print_request_info(request)

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
  # this method has a side effect, so get is not the best way to go;
  # and make sure you redirect to another page when there is a POST
  inserted_name = request.GET.get('name', None)
  if inserted_name:
    return render(
        request, 'monitor/insert_symbol_form.html',
        {
          'inserted':True,
          'inserted_symbol_name':inserted_name,
        }
      )
  return render(
      request, 'monitor/insert_symbol_form.html',
    )

def contact(request):
  errors  = []
  if request.method == 'POST':
    if not request.POST.get('subject', ''):
      errors.append('Enter a subject.')
    if not request.POST.get('message', ''):
      errors.append('Enter a message')
    if request.POST.get('email') and '@' not in request.POST['email']:
      errors.append('Enter a valid e-mail address.')
    if not errors:
      send_mail(
          request.POST['subject'],
          request.POST['message'],
          request.POST.get('email', 'noreply@example.com'),
          ['siteowner@example.com'],
        )
      return HttpResponseRedirect('/contact/thanks/')
  return render(
      request, 'monitor/contact_form.html', {'errors':errors}
    )
