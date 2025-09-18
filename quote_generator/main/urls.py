from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('register/', views.register, name='register'),
    path('logIn/', views.logIn, name='logIn'),
    path('like/', views.like_quote, name='like_quote'),
    path('logout/', views.logout, name='logout'),
    path('addquote/', views.add_quote, name='add_quote'),
    path('top_quotes/', views.popluar, name='top_quotes'),
    path('dislike/', views.dislike_quote, name='dislike_quote')
]