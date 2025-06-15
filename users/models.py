from django.contrib.auth.models import User
from django.db import models
from trips.models import Trip
from django.core.validators import URLValidator, MaxLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    cover_photo = models.ImageField(upload_to='cover_photos/', default='cover_photos/default.png')
    bio = models.TextField(blank=True, validators=[MaxLengthValidator(300)])
    is_verified = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    favorites = models.ManyToManyField(Trip, related_name='favorited_by', blank=True)

    facebook_username = models.CharField(max_length=100, blank=True)
    instagram_username = models.CharField(max_length=100, blank=True)

    facebook_url = models.CharField(max_length=255, blank=True, editable=False)
    instagram_url = models.CharField(max_length=255, blank=True, editable=False)

    whatsapp_number = PhoneNumberField(blank=True, region='EG')
    phone_number = PhoneNumberField(blank=True, region='EG')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def has_any_contact(self):
        return any([
            self.facebook_url,
            self.instagram_url,
            self.whatsapp_number,
            self.phone_number,
        ])

    def save(self, *args, **kwargs):


        # Phone numbers: ensure they start with +20
        if self.whatsapp_number:
            raw = str(self.whatsapp_number)
            if not raw.startswith('+20'):
                raw = f'+20{raw.lstrip("0")}'
            self.whatsapp_number = PhoneNumber.from_string(raw, region='EG')

        if self.phone_number:
            raw = str(self.phone_number)
            if not raw.startswith('+20'):
                raw = f'+20{raw.lstrip("0")}'
            self.phone_number = PhoneNumber.from_string(raw, region='EG')

        super().save(*args, **kwargs)
