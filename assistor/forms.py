from django import forms
from django.forms import EmailInput, PasswordInput, TextInput, DateInput
from .models import Course, File, Note, Reminder, User, Link, Instructor

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

class LoginForm(forms.Form):
    # Username
    username = forms.CharField(max_length=150, required=True, widget=TextInput(attrs={"class": "form-control form-control-sm"}))

    # Password
    password = forms.CharField(max_length=128, required=True, widget=PasswordInput(attrs={"class": "form-control form-control-sm"}))


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "start_date", "completion_date", "grade", "provider"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control form-control-sm"}),
            "start_date": DateInput(attrs={"class": "form-control form-control-sm", "type": "datetime-local"}),
            "completion_date": DateInput(attrs={"class": "form-control form-control-sm", "type": "datetime-local"}),
            "grade": TextInput(attrs={"class": "form-control form-control-sm"}),
            "provider": TextInput(attrs={"class": "form-control form-control-sm"})
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control form-control-sm"}),
            "content": forms.Textarea(attrs={"class": "form-control form-control-sm"})
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "category" , "file"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control form-control-sm"}),
            "category": forms.Select(attrs={
                "class": "form-select form-select-sm",
                "aria-label": ".form-select-sm"
                }),
            "file": forms.FileInput(attrs={"class": "form-control form-control-sm"})
        }

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ["name", "url"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control form-control-sm"}),
            "url": forms.URLInput(attrs={"class": "form-control form-control-sm"})
        }

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ["title", "first_name", "last_name", "email"]
        widgets = {
            "title": forms.Select(attrs={
                "class": "form-select form-select-sm",
                "aria-label": ".form-select-sm"
                }),
            "first_name": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "last_name": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["name", "time"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "time": forms.DateTimeInput(attrs={"class": "form-control form-control-sm", "type": "datetime-local"})
        }