from django.urls import path
from . import views

urlpatterns = [
    path('', views.petition_list, name='petition_list'),
    # path('add/', views.add_petition, name='add_petition'),
    # path('submit/', views.submit_petition, name='submit_petition'),
    path('vote/<int:petition_id>/', views.vote_petition, name='vote_petition'),
]