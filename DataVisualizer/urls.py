from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.upload,name='upload'),
    path('viewcsv', views.viewcsv, name='viewcsv'),
    path('viewgraph', views.viewgraph, name='showgraph')

]
