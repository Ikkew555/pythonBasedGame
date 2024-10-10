from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start_game/<str:level>/', views.start_game, name='start_game'),
    path('match_card/<int:card_index>/', views.match_card, name='match_card'),
    path('submit_score/', views.submit_score, name='submit_score'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('reset_game/', views.reset_game, name='reset_game'),
    path('congratulations/', views.congratulations, name='congratulations'),  # Add this line
    path('clear-leaderboard/', views.clear_leaderboard, name='clear_leaderboard'),
    ]
