from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^overview/(?P<pk>\d+)/$', views.Overview.as_view(),
        name='logframe-overview'),

    url(r'^output/$', views.OutputCreate.as_view(),
        name='logframe-output-create'),

    url(r'^output/(?P<pk>\d+)/?$', views.OutputUpdate.as_view(),
        name='logframe-output-update'),
)
