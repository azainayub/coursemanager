from django.http import response
from django.test import TestCase, Client
from django.db import IntegrityError

from .views import index
from .models import Course, User

class RegistrationTestCase(TestCase):
    def test_user_should_register(self):
        """Check a user should register account"""
        c = Client()
        c.post("/register", {"first_name":"Azain", "last_name":"Ayub", "username" : "azainayub",
        "email":"azain.ayub2014@gmail.com", "password":"azain", "confirmation": "azain"})
        self.assertEquals(User.objects.all().count(), 1)

class LoginTestCase(TestCase):
    def setUp(self):
        # Dummy users
        User.objects.create_user(first_name="Azain", last_name="Ayub", username = "azainayub",
        email="azain.ayub2014@gmail.com", password="azain")
        User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")

    def test_login_using_get(self):
        """Check login renders successfully using get"""
        c = Client()
        response = c.get("/login")
        self.assertEquals(response.status_code, 200)

    def test_login_valid_user(self):
        """Check a user can login"""
        c = Client()
        response = c.post("/login", {"username": "admin", "password": "admin"})
        self.assertTrue(response.status_code, 302)
        
    def test_login_invalid_user(self):
        """Check an invalid user should not log in"""
        c = Client()
        response = c.post("/login", {"username": "hello", "password": "world"})
        self.assertEquals(response.context.get("message"), "Invalid username and/or password.")

class CourseTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user = User.objects.create_user(first_name="Azain", last_name="Ayub", username = "azainayub",
        email="azain.ayub2014@gmail.com", password="azain")
        Course.objects.create(user=user, title="Software Construction and Development")
        Course.objects.create(user=user, title="Human Computer Interaction")
    
    def test_course_should_be_accessible(self):
        """Check a course can be accessed by authorized user"""
        c = Client()
        c.login(username="azainayub", password="azain")
        response = c.get("/courses/" + str(Course.objects.get(title ="Human Computer Interaction").id))
        self.assertEquals(response.status_code, 200)

    def test_course_should_not_be_accessible(self):
        """Check a course is not accessible for unauthorized user"""
        c = Client()
        c.login(username="admin", password="admin")
        response = c.get("/courses/" + str(Course.objects.get(title ="Human Computer Interaction").id))
        self.assertEquals(response.status_code, 403)


