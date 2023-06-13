from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=50, verbose_name="모집 프로그램명")
    content = models.TextField(verbose_name="모집 프로그램 상세 설명")
    information = models.TextField(null=True, blank=True, verbose_name="합격 메시지(선발된 사용자에게만 보임)")

    question1 = models.CharField(max_length=100, null=True, blank=True, verbose_name="지원서 첫 번째 질문")
    question2 = models.CharField(max_length=100, null=True, blank=True, verbose_name="지원서 두 번째 질문")
    question3 = models.CharField(max_length=100, null=True, blank=True, verbose_name="지원서 세 번째 질문")
    is_finish = models.BooleanField(default=False)

    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/meeting/{self.pk}"
