from typing_extensions import ParamSpec
from django import forms
from django.forms import widgets
from .models import Course, File, Note, Reminder

class NewCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title"]
        labels = {
            "content": "New Post"
        }
        widgets = {

        }

class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        labels = {
            "title": "Title",
            "content": "Content"
        }

class NewFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file"]
        labels = {
            "name": "Name",
            "file": "File"
        }

class NewReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["name", "time"]
        labels = {
            "name": "Name",
            "time": "Time"
        }
