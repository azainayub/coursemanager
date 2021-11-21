from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

class Course(models.Model):
    # User who created the course
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)

    # Title of the course
    title = models.CharField(max_length=60 , null=False, blank=False)

    # Time of creation
    time = models.DateTimeField(auto_now=True, null=False, blank=True)

    def __str__(self):
        return f"{self.title} by {self.user}"

class Note(models.Model):
    # The course note belongs to
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=True, related_name="notes")

    # Title of the note
    title = models.CharField(max_length=60, null=False, blank=False)

    # Content of the note
    content = models.CharField(max_length=2048 , null=False, blank=False)

    def __str__(self):
        return f"{self.title}"
