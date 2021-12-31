from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

class Course(models.Model):
    # User who created the course
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True, related_name="courses")

    # Title of the course
    title = models.CharField(max_length=64 , null=False, blank=False)

    # Time of creation
    creation_time = models.DateTimeField(auto_now=True, null=False, blank=True)

    def __str__(self):
        return f"{self.title} by {self.user}"

class Note(models.Model):
    # The course note belongs to
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=True, related_name="notes")

    # Title of the note
    title = models.CharField(max_length=64, null=False, blank=False)

    # Content of the note
    content = models.CharField(max_length=2048 , null=False, blank=False)

    # Time of creation
    creation_time = models.DateTimeField(auto_now=True, null=False, blank=True)

    def __str__(self):
        return f"{self.title}"

class File(models.Model):
    # The course where file belongs
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=True, related_name="files")

    # Name of the file
    name = models.CharField(max_length=255, null=False, blank=False)

    # File
    file = models.FileField(null=False, blank=False)

    # Time of creation
    creation_time = models.DateTimeField(auto_now=True, null=False, blank=True)

class Reminder(models.Model):
    # The user who added reminder
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True, related_name="reminders")

    # Name of the reminder
    name = models.CharField(max_length=64, null=False, blank=False)

    # Time of the reminder
    time = models.DateTimeField(null=False, blank=False)

    # Time of creation
    creation_time = models.DateTimeField(auto_now=True, null=False, blank=True)

