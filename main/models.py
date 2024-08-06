from django.db import models
from users.models import *
from groups.models import *
from django.utils import timezone

# 열람시간 저장 모델 + 각 유저마다 시간을 다르게 볼 수 있도록
class openTime(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    morning_time = models.TimeField(default='05:00:00')
    night_time = models.TimeField(default='21:00:00')

    def __str__(self):
        return f"모닝메세지: {self.morning_time}, 나잇메세지: {self.night_time}"

# 메세지 작성 모델
class Message(models.Model):
    nick = models.ForeignKey(Profile, on_delete=models.CASCADE)
    morning_mes = models.CharField(max_length=200)
    night_mes = models.CharField(max_length=200)
    created_at = models.DateTimeField('date published', default = timezone.now)
    morninglikes = models.ManyToManyField(Profile, related_name='morning_liked_messages', blank=True)
    nightlikes = models.ManyToManyField(Profile, related_name='night_liked_messages', blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        return f"{self.morning_mes}, {self.night_mes}"
    def total_morning_likes(self):
        return self.morninglikes.count()

    def total_night_likes(self):
        return self.nightlikes.count()
    
# 알람데이터 저장 모델
# ForeignKey로 User를 하는 이유는, Profile모델은 User 기본모델을 참조하며 추가적인 부분을 작성하는 보조모델이기 때문에 더 직관적으로 사용자와 알림간의 관계를 정의하려면 User를 참조해야한다.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message