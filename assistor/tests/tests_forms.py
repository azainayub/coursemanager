from datetime import date, datetime
from django.test import TestCase, client

from assistor.models import User, Course, Note
from assistor.forms import CourseForm, NoteForm, FileForm, LinkForm, InstructorForm, ReminderForm, RegistrationForm, LoginForm

class CourseFormTestCase(TestCase):
    """Test the course form"""

    def test_valid_course_data(self):
        """Check the form with valid data"""
        form_data = {
            "title": "Information Security", 
            "start_date": date(2022, 2, 28),
            "completion_date": date(2022, 7, 3),
            "grade": ["A"],
            "provider": "X University"
        }
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_course_data(self):
        """Check the form with invalid data"""
        # Missing title
        form_data = {
            "start_date": date(2022, 2, 28),
            "completion_date": date(2022, 7, 3),
            "grade": ["A"],
            "provider": "X University"
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())

class NoteFormTestCase(TestCase):
    """Test the note form"""

    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@...", password="admin")
        user.save()
        course = Course.objects.create(user=user, title="Information Security")
        course.save()

    def test_valid_note_data(self):
        """Check the form with valid data"""
        form_data = {
            "title": "Lorem Ipsum",
            "content": "Lorem Ipsum sit amet ......"
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_note_data(self):
        """Check the form with invalid data"""
        # Missing title and title exceeding max length
        form_data = {
            "title": """Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum
            Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum
            Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum
            Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum
            Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum
            Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum""",
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())

class FileFormTestCase(TestCase):
    """Test the file form"""

    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@...", password="admin")
        user.save()
        course = Course.objects.create(user=user, title="Information Security")
        course.save()

    def test_valid_file_data(self):
        """Check the form with valid data"""
        pass
    
    def test_invalid_file_data(self):
        """Check the form with invalid data"""
        pass
