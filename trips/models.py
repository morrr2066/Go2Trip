from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import date
from PIL import Image


class Trip(models.Model):
    title = models.CharField(max_length=60)
    max_persons = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999999)])
    price = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 9999.99 max price
    trip_date_start = models.DateField()
    trip_date_end = models.DateField()
    city = models.CharField(max_length=20)
    description = models.TextField(help_text="Describe all places you will visit")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_picture = models.ImageField(upload_to='trip_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes(self):
        return self.favorited_by.count()

    @property
    def trip_duration(self):
        delta = (self.trip_date_end - self.trip_date_start).days + 1
        return max(delta, 0)

    @property
    def days_until_trip(self):
        delta = (self.trip_date_start - date.today()).days
        return max(delta, 0)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first so image file is available

        if self.trip_picture:
            try:
                img = Image.open(self.trip_picture.path)
                img = img.convert('RGB')
                img = img.resize((200, 200), Image.LANCZOS)
                img.save(self.trip_picture.path, format='JPEG', quality=90)
            except Exception as e:
                # Just log the error, but don't stop saving
                print(f"Image processing error: {e}")