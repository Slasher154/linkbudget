from django.conf.urls import patterns, include, url
from mysite import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from linkbudget import views as lbviews

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', views.welcome, name='welcome'),
                       url(r'^index/$', views.index, name='home'),
                       url(r'^deploy/$', views.deploy, name='deploy'),
                       url(r'^progress/$', views.progress, name='progress'),
                       url(r'^testjson/$', views.testjson, name='testjson'),

                       # Include URLs for link budget applications
                       url(r'^linkbudget/', include('linkbudget.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),


)

