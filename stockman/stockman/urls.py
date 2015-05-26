from django.conf.urls import patterns, include, url
from django.contrib import admin

from monitor.views import hello as monitor_hello
from monitor.views import insert_symbol, contact

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stockman.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^hello/$', monitor_hello),
    url(r'^insert_symbol/$', insert_symbol),
    url(r'contact/$', contact),
    url(r'^admin/', include(admin.site.urls)),
)
