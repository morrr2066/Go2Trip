from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    title = models.CharField(max_length=200)
    max_persons = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 9999.99 max price
    trip_date = models.DateField()
    destinations = models.TextField(help_text="Describe all places you will visit")
    contact_info = models.CharField(max_length=100)  # phone or email
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
