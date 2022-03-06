from datetime import date, datetime
from turtle import title
from django.test import TestCase

from assistor.models import Course, User, Note, File, Link, Instructor, Reminder

class CourseTestCase(TestCase):
    """Test the course model"""

    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@...", password="admin")
        user.save()

    def test_course_is_created(self):
        """Check a course is created"""
        user = User.objects.get(username="admin")
        course = Course.objects.create(
            user=user, 
            title="Information Security", 
            start_date=date(2022, 2, 28),
            completion_date=date(2022, 7, 3),
            grade=["A"],
            provider="X University"
        )
        course.save()
        self.assertEqual(Course.objects.count(), 1)

class NoteTestCase(TestCase):
    """Test the note model"""

    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@...", password="admin")
        user.save()
        course = Course.objects.create(
            user=user, 
            title="Information Security", 
            start_date=date(2022, 2, 28),
            completion_date=date(2022, 7, 3),
            grade=["A"],
            provider="X University"
        )
        course.save()

    def test_note_is_created(self):
        """Check a note is created"""
        user = User.objects.get(username="admin")
        course = Course.objects.get(title="Information Security")
        note = Note.objects.create(course=course, title="Lorem Ipsum", content="Lorem Ipsum sit amet...........")
        note.save()
        self.assertEqual(Note.objects.count(), 1)

class FileModelTestCase(TestCase):
    pass