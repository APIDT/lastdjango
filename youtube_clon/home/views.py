from django.shortcuts import render, get_object_or_404
from videos.models import Video

def index(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'home/index.html', {'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'home/video_detail.html', {'video': video})
