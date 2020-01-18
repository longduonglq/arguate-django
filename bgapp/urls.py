from django.urls import path, include
from . import views

urlpatterns = [
    path('topics/', views.get_topics),
    path('user_topics/', views.get_user_topics)
]
