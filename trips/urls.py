from django.urls import path
from . import views
from .views import trip_search_view


#app_name = 'trips'

urlpatterns = [
    path('', views.home, name='home'),  # trips homepage
    path('create/', views.create_trip, name='create'),
    path('trip/delete/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    path('trip/<int:trip_id>/edit/', views.edit_trip, name='edit_trip'),
    path('search/', trip_search_view, name='trip_search'),
    path('toggle-favorite/<int:trip_id>/', views.toggle_favorite, name='toggle_favorite'),  # updated here
    path('trip/<int:trip_id>/trip_details/', views.trip_details, name='trip_details'),
]
