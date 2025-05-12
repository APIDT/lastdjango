# videos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('<int:video_id>/', views.video_detail, name='video_detail'),
    path('<int:video_id>/delete/', views.delete_video, name='delete_video'),
    path('<int:video_id>/vote/', views.process_vote, name='process_vote'),
    path('video/<int:video_id>/add_comment/', views.add_comment, name='add_comment'),
    path('search/', views.search_videos, name='search_videos'),
]