from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    list = models.ForeignKey('List', related_name='tasks', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.title
    
class List(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100, default='To-Do List')
    owner = models.ForeignKey(Profile, related_name='lists', on_delete=models.CASCADE, null=False, blank=False)
   
    def __str__(self):
        return self.name