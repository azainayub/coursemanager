import email
from pyexpat import model
from statistics import mode
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey

from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # First name of the user
    first_name = models.CharField(max_length=64 , null=False, blank=False)

    # Last name of the user
    last_name = models.CharField(max_length=64, null=False, blank=False)

    # Email of the user account
    email = models.CharField(max_length=256, null=False, blank=False, unique=True)



class Course(models.Model):
    # User who created the course
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True, related_name="courses")

    # Title of the course
    title = models.CharField(max_length=64 , null=False, blank=False)

    # Start date of the course
    start_date = models.DateField(null=True, blank=True)

    # Completion date of the course
    completion_date = models.DateField(null=True, blank=True)

    # Grade of the course
    grade = models.CharField(max_length=8 , null=True, blank=True)

    # Course provider
    provider = models.CharField(max_length=256 , null=True, blank=True)

    # Time of creation
    creation_time = models.DateTimeField(auto_now=True, null=False, blank=True)

    def __str__(self):
        return f"{self.title} by {self.user}"

class Instructor(models.Model):
    # The course taught by instructor
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=True, related_name="instructors")
    
    class Titles(models.TextChoices):
        # Titles
        DOCTOR = "DR", _("Dr.")
        HONORABLE = "HO", _("Hon.")
        JUNIOR = "JR", _("Jr.")
        MISTER = "MR", _("Mr.")
        MISSES = "MS", _("Mrs.")
        MISS = "MI", _("Ms.")
        PROFESSOR = "PR", _("Prof.")
        SENIOR = "SR", _("Sr.")

    title = models.CharField(max_length=2, choices=Titles.choices, default=Titles.PROFESSOR, null=False, blank=False)

    # First Name
    first_name = models.CharField(max_length=64, null=False, blank=False)

    # Last Name
    last_name = models.CharField(max_length=64, null=True, blank=True)

    # Email of the Instructor
    email = models.EmailField(max_length=256, null=True, blank=True, unique=True)

    def get_name(self):
        return self.title.label + " " + self.first_name + " " + self.last_name

class Note(models.Model):
    # The course note belongs to
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=True, related_name="notes")

    # Title of the note
    title = models.CharField(max_length=64, null=False, blank=False)

    # Content of the note
    content = models.CharField(max_length=8192 , null=False, blank=False)

    # Time of creation
    creation_time = models.DateTimeField(auto_now=True, null=False, blank=True)

    def __str__(self):
        return f"{self.title}"

class File(models.Model):
    # The course where file belongs
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=True, related_name="files")

    # Name of the file
    name = models.CharField(max_length=255, null=False, blank=False)

    # Categories
    ASSIGNMENT = "AS"
    DOCUMENT = "DO"
    JOURNAL = "JO"
    QUIZ = "QU"
    SLIDES = "SL"
    OTHER = "OT"

    CATEGORIES = [
        (ASSIGNMENT, "Assignment"),
        (DOCUMENT, "Document"),
        (JOURNAL, "Journal"),
        (QUIZ, "Quiz"),
        (SLIDES, "Slides"),
        (OTHER, "Other"),
    ]

    catergory = models.CharField(max_length=2, choices=CATEGORIES, default=OTHER, null=False, blank=False)

    # File
    file = models.FileField(null=False, blank=False)

    # Time of creation
    creation_time = models.DateTimeField(auto_now=True, null=False, blank=True)

class Link(models.Model):
    # The course the link belongs to
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=True, related_name="links")

    # Name of the link
    name = models.CharField(max_length=256, null=False, blank=False)

    # URL
    url = models.URLField(max_length=2048, null=False, blank=False)

    # Time of creation
    creation_time = models.DateTimeField(auto_now=True, null=False, blank=True)

class Reminder(models.Model):
    # The user who added reminder
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True, related_name="reminders")

    # Name of the reminder
    name = models.CharField(max_length=256, null=False, blank=False)

    # Time of the reminder
    time = models.DateTimeField(null=False, blank=False)

    # Time of creation
    creation_time = models.DateTimeField(auto_now=True, null=False, blank=True)

