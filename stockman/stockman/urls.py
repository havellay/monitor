from django.conf.urls import patterns, include, url
from django.contrib import admin

from monitor.views import print_request_info, insert_symbol, insert_trigger

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stockman.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^print_request_info/$', print_request_info),
    url(r'^insert_symbol/$',      insert_symbol),
    url(r'^insert_trigger/$',     insert_trigger),

    url(r'^admin/', include(admin.site.urls)),
)
