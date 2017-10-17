from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^data/', views.db_operations, name='db_operations'),
    url(r'^present/', views.data_visualization, name='data_visualization'),
]
