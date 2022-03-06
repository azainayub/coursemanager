from datetime import date, datetime
from django.test import TestCase, client

from assistor.models import User, Course
from assistor.forms import CourseForm, LinkForm, InstructorForm, ReminderForm

class CourseFormTestCase(TestCase):
    """Test the course form"""

    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@...", password="admin")
        user.save()

    def test_valid_course_data(self):
        """Check the form with valid data"""
        user = User.objects.get(username="admin")
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
        user = User.objects.get(username="admin")
        # Missing title
        form_data = {
            "start_date": date(2022, 2, 28),
            "completion_date": date(2022, 7, 3),
            "grade": ["A"],
            "provider": "X University"
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())