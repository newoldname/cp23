from django.db import models
from django.contrib.auth.models import User

from meeting.models import Project


# Create your models here.
class Application(models.Model):
    answer1 = models.TextField(null=True, blank=True)
    answer2 = models.TextField(null=True, blank=True)
    answer3 = models.TextField(null=True, blank=True)

    is_apply = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Project, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.pk}]-{self.author}의 지원서"

    def get_absolute_url(self):
        return f"/meeting/"
