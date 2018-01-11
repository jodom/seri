from django.conf.urls import url
from . import views

# series urls
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^serie/new_serie/$', views.new_serie, name='new_serie'),
]
