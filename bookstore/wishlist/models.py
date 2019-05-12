from django.db import models
from django.utils import timezone
from users.models import Profile
from bookDetails.models import Book

# date_created = models.DateTimeField(default=datetime.now, blank=True) from datetime import datetime
class List(models.Model):
    name = models.CharField(max_length=25)
    date_created = models.DateTimeField(default=timezone.now, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('user', 'date_created')