from django.test import TestCase, Client

from .views import index
from .models import Course, User

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

