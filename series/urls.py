from django.conf.urls import url
from . import views

# series urls
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^serie/new/$', views.new_serie, name='new_serie'),
    url(r'^serie/(?P<pk>\d+)/$', views.serie_detail, name='serie_detail'),
]
