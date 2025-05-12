from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
]
