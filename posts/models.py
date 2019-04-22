from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Hashtag(models.Model):
    content = models.TextField(unique=True)    # 같은 text면 하나만 생겨야 함
    
    def __str__(self):
        return self.content
        

class Post(models.Model):
    # user : post 를 1:N 관계로 설정
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user.post_set.all() - 게시글? 좋아요 한 글?
    # 게시글 입장에서 나를 좋아요 한 유저들 - like_users : 변수 명시적으로 정함
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts', blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)     # 복수형으로 하는 것이 좋음
    content = models.TextField()
    
    def __str__(self):
        return self.content
        
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)    # CASCADE : 게시글 하나가 삭제되면 전체 사진이 삭제됨
    file = ProcessedImageField(
                upload_to='posts/images',					# 저장 위치
                processors=[ResizeToFill(600, 600)],		# 처리할 작업 목록
                format='JPEG',								# 저장 포맷
                options={'quality': 90},					# 옵션 - 화질
    		)
    		
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    
    def __str__(self):
        return self.content