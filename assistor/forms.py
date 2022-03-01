from django import forms
from django.forms import EmailInput, PasswordInput, TextInput, DateInput
from .models import Course, File, Note, Reminder, User

class RegistrationForm(forms.ModelForm):
    error_css_class = 'text-danger'
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
        widgets = {
            "first_name": TextInput(attrs={"class": "form-control form-control-sm"}),
            "last_name": TextInput(attrs={"class": "form-control form-control-sm"}),
            "username": TextInput(attrs={"class": "form-control form-control-sm"}),
            "email": EmailInput(attrs={"class": "form-control form-control-sm"}),
            "password": PasswordInput(attrs={"class": "form-control form-control-sm"})
        }

class LoginForm(forms.ModelForm):
    class Meta:
        error_css_class = 'text-danger'
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": TextInput(attrs={"class": "form-control form-control-sm"}),
            "password": PasswordInput(attrs={"class": "form-control form-control-sm"})
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "start_date", "completion_date", "grade", "provider"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control form-control-sm"}),
            "start_date": DateInput(attrs={"class": "form-control form-control-sm"}),
            "completion_date": DateInput(attrs={"class": "form-control form-control-sm"}),
            "grade": TextInput(attrs={"class": "form-control form-control-sm"}),
            "provider": TextInput(attrs={"class": "form-control form-control-sm"})
        }

class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        labels = {
            "title": "Title",
            "content": "Content"
        }
        widgets = {
            "content": forms.Textarea()
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
        widgets = {
            "time": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }