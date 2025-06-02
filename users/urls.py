from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),   # updated here
    path('logout/', views.logout_view, name='logout'), # updated here
    path('profile/',views.profile_view,name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
