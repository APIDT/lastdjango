from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse  # Для кращого формування URL-адрес
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed  # Для обробки прав доступу та методів
from django.views.decorators.http import require_POST  # Для обмеження методу запиту

from .models import Video, LikeDislike, Comment
from .forms import VideoForm, CommentForm  # Додано CommentForm

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect('video_detail', video_id=video.id)
    else:
        form = VideoForm()
    return render(request, 'home/upload.html', {'form': form})

def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    comments = video.comments.all().order_by('-created_at')  # Отримуємо коментарі
    
    user_reaction = None
    if request.user.is_authenticated:
        try:
            user_reaction = LikeDislike.objects.get(user=request.user, video=video)
        except LikeDislike.DoesNotExist:
            user_reaction = None

    if request.method == 'POST' and request.user.is_authenticated:
        # Обробка додавання коментаря
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.video = video
            new_comment.save()
            return redirect('video_detail', video_id=video.id) 
    else:
        comment_form = CommentForm()  # Форма для GET запиту або якщо користувач не автентифікований

    context = {
        'video': video,
        'likes_count': video.get_likes_count,
        'dislikes_count': video.get_dislikes_count,
        'user_reaction': user_reaction,  # Передаємо об'єкт реакції або None
        'comments': comments,
        'comment_form': comment_form,  # Передаємо форму для коментаря
    }
    return render(request, 'video_detail.html', context)

@login_required  # Голосувати можуть тільки авторизовані користувачі
@require_POST  # Це представлення повинно приймати тільки POST запити
def process_vote(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    vote_type = None

    if 'like' in request.POST:
        vote_type = LikeDislike.LIKE
    elif 'dislike' in request.POST:
        vote_type = LikeDislike.DISLIKE
    else:
        # Якщо не було передано ні 'like', ні 'dislike', це невалідна ситуація
        return redirect('video_detail', video_id=video.id)

    reaction, created = LikeDislike.objects.get_or_create(
        user=request.user, 
        video=video,
        defaults={'value': vote_type}  # Встановлюємо значення за замовчуванням, якщо об'єкт створюється
    )

    if not created:
        # Якщо реакція вже існувала
        if reaction.value == vote_type:
            # Користувач натиснув ту саму кнопку (наприклад, лайк на вже лайкнуте) - видаляємо реакцію
            reaction.delete()
        else:
            # Користувач змінив свою думку (наприклад, з дізлайка на лайк) - оновлюємо значення
            reaction.value = vote_type
            reaction.save()

    return redirect('video_detail', video_id=video.id)

@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if video.user == request.user:
        video.delete()
        return redirect('home')  # Перенаправлення на домашню сторінку або список відео
    else:
        # Користувач не є власником відео, забороняємо видалення
        return HttpResponseForbidden("Ви не можете видалити це відео.")

@login_required
def add_comment(request, video_id):
    video = Video.objects.get(id=video_id)
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
            return redirect('video_detail', video_id=video.id)  # Переадресація на сторінку відео
    return redirect('video_detail', video_id=video.id)

def search_videos(request):
    query = request.GET.get('q')
    videos = Video.objects.filter(title__icontains=query)
    return render(request, 'home/search_results.html', {'videos': videos})