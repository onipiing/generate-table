from django.conf.urls import url
from website import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^create_table/$', views.create_table, name="create_table"),
]
