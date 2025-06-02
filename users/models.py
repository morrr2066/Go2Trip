from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    cover_photo = models.ImageField(upload_to='cover_photos/', default='cover_photos/default.png')
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)  # <--- Add this

    def __str__(self):
        return f"{self.user.username}'s Profile"