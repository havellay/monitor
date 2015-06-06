from django.conf.urls import patterns, include, url
from django.contrib import admin

from monitor.views import print_request_info, insert_symbol, insert_reminder, scratch, get_form, get_attrib_form, get_triggered_reminders, provide_monitorjs

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stockman.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^insert_symbol/$', insert_symbol),
    url(r'^insert_reminder/$', insert_reminder),

    url(r'^get_attrib_form', get_attrib_form),
    url(r'^get_triggered_reminders/$', get_triggered_reminders),

    url(r'^scripts/monitor.js', provide_monitorjs),

    url(r'^print_request_info/$', print_request_info),
    url(r'^scratch/$', scratch),
    url(r'^get_form/$', get_form),

    url(r'^admin/', include(admin.site.urls)),
)
