from turtle import title
from unicodedata import category
from urllib import response
from django.test import TestCase, Client
from django.contrib.auth import login
from django.urls import reverse
from django.db.models import Max

from assistor.views import index
from assistor.models import Course, User

class RegistrationTestCase(TestCase):
    def test_user_registers_with_valid_data(self):
        """Check user successfully registers with valid data"""
        c = Client()
        response = c.post("/register", {"first_name":"Azain", "last_name":"Ayub", "username" : "azainayub",
        "email":"azain.ayub2014@gmail.com", "password":"azain", "confirmation": "azain"})
        self.assertEqual(response.status_code, 302)

    def test_user_register_fails_without_first_name(self):
        """Check registration fails without first name"""
        c = Client()
        response = c.post("/register", {"last_name":"Ayub", "username" : "azainayub",
        "email":"azain.ayub2014@gmail.com", "password":"azain", "confirmation": "azain"})
        self.assertNotEqual(response.status_code, 302)

    def test_user_register_fails_without_email(self):
        """Check registration fails without email name"""
        c = Client()
        response = c.post("/register", {"first_name":"Azain", "last_name":"Ayub", "username" : "azainayub", 
        "password":"azain", "confirmation": "azain"})
        self.assertNotEqual(response.status_code, 302)

    def test_user_register_fails_without_username(self):
        """Check registration fails without username"""
        c = Client()
        response = c.post("/register", {"first_name":"Azain", "last_name":"Ayub", "email":"azain.ayub2014@gmail.com", 
        "password":"azain", "confirmation": "azain"})
        self.assertNotEqual(response.status_code, 302)

    def test_user_register_fails_without_same_password_confirmation(self):
        """Check registration fails without same password and confirmation"""
        c = Client()
        response = c.post("/register", {"first_name":"Azain", "last_name":"Ayub", "email":"azain.ayub2014@gmail.com", 
        "password":"azaina", "confirmation": "azainb"})
        self.assertNotEqual(response.status_code, 302)

class LoginViewTestCase(TestCase):
    """
    Test the login view
    """
    def setUp(self):
        # Create some dummy users
        User.objects.create_user(first_name="Azain", last_name="Ayub", username = "azain",
        email="azainayub@...", password="azain")
        User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@...", password="admin")

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
        self.assertEquals(response.context.get("message"), "Failed to login!")

    def test_login_incorrect_password(self):
        """Check user should not login with incorrect password"""
        c = Client()
        response = c.post("/login", {"username": "azainayub", "password": "abc"})
        self.assertEquals(response.context.get("message"), "Failed to login!")

class CourseViewTestCase(TestCase):
    """
    Test the course view
    """
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

class NewFileViewTestCase(TestCase):
    """
    Test the new file view
    """
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        course = Course.objects.create(user=user, title="Human Computer Interaction")
        user.save()
        course.save()

    def test_new_file_logged_out(self):
        """Check a logged out user should not access new file"""
        course = Course.objects.get(title="Human Computer Interaction")
        response = self.client.get(reverse("file_new", args={course.id}))
        self.assertRedirects(response, "/login?next=/courses/1/files/new")

    def test_new_file_logged_in(self):
        """Check a logged in user access new file"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Human Computer Interaction")
        response = self.client.get(reverse("file_new", args={course.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("course"), course)
        self.assertTemplateUsed("assistor/file_new.html")

    def test_new_file_invalid_course_id(self):
        """Check a new file should return 404 for invalid course id"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("file_new", args={Course.objects.filter().aggregate(Max('id')).get('id__max') + 1}))
        self.assertTrue(response.status_code, 404)

    def test_new_file_adds_file(self):
        """Check an authorised user can add new file"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Human Computer Interaction")
        with open("assistor/templates/assistor/index.html") as tf:
            response = self.client.post(reverse("file_new", args={course.id}), {
                "name": "TestFile", 
                "category": ['AS'],
                "file": tf
            }, 
            format='multipart/form-data')
        self.assertRedirects(response, reverse("course", args={course.id}))