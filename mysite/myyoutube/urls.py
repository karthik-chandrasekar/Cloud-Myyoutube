from django.conf.urls import patterns, include, url

urlpatterns = patterns('myyoutube.views',
    url(r'^index/', 'index'),
    #url(r'^display/', 'display'),
)
