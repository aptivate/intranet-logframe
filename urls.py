from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^output/$', views.OutputCreate.as_view(), name='logframe-output-create'),
)
