from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.map_index, name='insights.map'),
    path('regions/', views.regions_json, name='insights.regions'),
    path('region/<int:id>/top/', views.region_top_json, name='insights.region_top'),
]

