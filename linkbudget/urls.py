__author__ = 'thanatv'

from django.conf.urls import patterns, include, url
from linkbudget import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='linkbudget_index'),
                       url(r'^result/$', views.result, name='linkbudget_result'),
)

