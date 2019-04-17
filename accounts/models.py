from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, blank=True)  # 처음에 빈값으로 만드는 것 허용하는 것
    introduction = models.TextField(blank=True)
    
    def __str__(self):
        return self.nickname
        
class User(AbstractUser):   # AbstractUser 상속받음
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')