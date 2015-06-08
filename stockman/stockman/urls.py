from django.conf.urls import patterns, include, url
from django.contrib import admin

from monitor import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stockman.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.get_index),

    url(r'^insert_symbol/$', views.insert_symbol),
    url(r'^insert_reminder/$', views.insert_reminder),

    url(r'^get_attrib_form', views.get_attrib_form),
    url(r'^get_triggered_reminders/$', views.get_triggered_reminders),

    # url(r'^scripts/monitor.js', provide_monitorjs),

    url(r'^print_request_info/$', views.print_request_info),
    url(r'^scratch/$', views.scratch),
    url(r'^get_form/$', views.get_form),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^(?P<dname>[a-z]+)/(?P<fname>[a-z.]+)', views.provide_script),
)
