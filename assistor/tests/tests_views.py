from turtle import title
from unicodedata import category, name
from urllib import response
from django.test import TestCase, Client
from django.contrib.auth import login
from django.urls import reverse
from django.db.models import Max

from assistor.views import index
from assistor.models import Course, User, File, Link, Instructor
from assistor.forms import LinkForm, InstructorForm

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
            response = self.client.post(reverse("file_new", args=[course.id]), {
                "name": "TestFile", 
                "category": ['AS'],
                "file": tf
            }, 
            format='multipart/form-data')
        self.assertRedirects(response, reverse("course", args={course.id}))

class EditFileTestCase(TestCase):
    """Test the edit file view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        course = Course.objects.create(user=user, title="Human Computer Interaction")
        user.save()
        course.save()

    def test_edit_file_renders(self):
        """Check the edit file view renders"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Human Computer Interaction")

        # Adding the file
        with open("assistor/templates/assistor/index.html") as tf:
            self.client.post(reverse("file_new", args=[course.id]), {
                "name": "TestFile", 
                "category": ['AS'],
                "file": tf
            }, 
            format='multipart/form-data')

        file = File.objects.get(name="TestFile")
        response = self.client.get(reverse("file_edit", args=[course.id, file.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("course"), course)
        self.assertEqual(response.context.get("file"), file)
        self.assertTemplateUsed("assistor/file_edit.html")

    def test_file_is_edit(self):
        """Check the file_edit view edits file"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Human Computer Interaction")

        # Adding the file
        with open("assistor/templates/assistor/index.html") as tf:
            self.client.post(reverse("file_new", args=[course.id]), {
                "name": "TestFile", 
                "category": ['AS'],
                "file": tf
            }, 
            format='multipart/form-data')
        
        file = File.objects.get(name="TestFile")

        # Edit the file
        with open("assistor/templates/assistor/index.html") as tf:
            response = self.client.post(reverse("file_edit", args=[course.id, file.id]), {
                    "name": "TestFileEdit", 
                    "category": ['AS'],
                    "file": tf
                }, 
                format='multipart/form-data')
        
        self.assertRedirects(response, reverse("file", args=[course.id, file.id]))

class NewLinkTestCase(TestCase):
    """Test the new link view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        course = Course.objects.create(user=user, title="Human Computer Interaction")
        user.save()
        course.save()

    def test_new_link_render(self):
        """Check the new link form renders"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Human Computer Interaction")
        response = self.client.get(reverse("link_new", args=[course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("course"), course)
        self.assertIsInstance(response.context.get("form"), LinkForm)
        self.assertTemplateUsed(response, "assistor/link_new.html")

    def test_new_link_is_created(self):
        """Check the new link is created"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Human Computer Interaction")
        response = self.client.post(reverse("link_new", args=[course.id]), {
            "name": "Test",
            "url": "https://www.google.com/"
        })
        self.assertRedirects(response, reverse("course", args=[course.id]))
        self.assertTrue(Link.objects.get(name="Test", course=course) != None)

class NewInstructorTestCase(TestCase):
    """Test the new instructor view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        course = Course.objects.create(user=user, title="Human Computer Interaction")
        user.save()
        course.save()

    def test_new_instructor_render(self):
        """Check the new instructor form renders"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Human Computer Interaction")
        response = self.client.get(reverse("instructor_new", args=[course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("course"), course)
        self.assertIsInstance(response.context.get("form"), InstructorForm)
        self.assertTemplateUsed(response, "assistor/instructor_new.html")

    def test_new_instructor_is_created(self):
        """Check the new instructor is created"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Human Computer Interaction")
        response = self.client.post(reverse("instructor_new", args=[course.id]), {
            "title": ["DR"],
            "first_name": "Hello",
            "last_name": "World",
            "email": "hello@world.com"
        })
        self.assertRedirects(response, reverse("course", args=[course.id]))
        self.assertTrue(Instructor.objects.get(email="hello@world.com", course=course) != None)
