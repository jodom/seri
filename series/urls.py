from django.conf.urls import url
from . import views

# series urls
urlpatterns = [
    url(r'^$', views.home, name='home'),
]
