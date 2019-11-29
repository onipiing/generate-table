from django.conf.urls import url
from website import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^create_table/$', views.create_table, name="create_table"),
    url(r'^download_table/$', views.download_table, name="download_table"),
    url(r'^error/$', views.error, name="error")
]
