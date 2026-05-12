from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Друзья
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/add-friend/', views.add_friend, name='add_friend'),
    path('users/<int:user_id>/remove-friend/', views.remove_friend, name='remove_friend'),
    path('friends/', views.friends_list, name='friends_list'),
]