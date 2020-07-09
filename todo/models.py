from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=40)
    memo = models.TextField(max_length=250, blank=True)
    importance = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    dateCompleted = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #This is one to maney relationship: One User has Many Todos

    def __str__(self):
        return self.title