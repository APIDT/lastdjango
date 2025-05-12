from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.conf import settings

class Video(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    # Видаляємо поля likes та dislikes, будемо розраховувати їх динамічно

    # Тепер ці методи є частиною класу Video
    @property
    def get_likes_count(self):
        """Повертає кількість лайків для цього відео."""
        return self.likedislike_set.filter(value=LikeDislike.LIKE).count()

    @property
    def get_dislikes_count(self):
        """Повертає кількість дізлайків для цього відео."""
        return self.likedislike_set.filter(value=LikeDislike.DISLIKE).count()

    def __str__(self):
        return self.title

class LikeDislike(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    # Можна додати опцію NONE, якщо хочемо явно зберігати відсутність реакції,
    # але зазвичай видалення запису є кращим підходом для "зняти лайк/дізлайк"
    VALUE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likedislike_set') # Додано related_name для ясності
    value = models.CharField(max_length=7, choices=VALUE_CHOICES)
    
    class Meta:
        # Унікальність, щоб користувач міг поставити тільки одну реакцію (лайк АБО дізлайк) на відео
        unique_together = ('user', 'video')

    def __str__(self):
        return f'{self.user.username} - {self.video.title} - {self.value}'

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments') # Додано related_name
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.video.title}'
    
def search_videos(request):
    query = request.GET.get('q', '')  # Отримуємо параметр пошуку з GET-запиту
    videos = Video.objects.filter(title__icontains=query)  # Пошук по назві відео
    
    return render(request, 'search_results.html', {'videos': videos, 'query': query})