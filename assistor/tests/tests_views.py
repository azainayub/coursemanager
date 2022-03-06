from datetime import date, datetime
from turtle import title
from unicodedata import name
from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Max

from assistor.views import index
from assistor.models import Course, User, File, Link, Instructor, Reminder, Note
from assistor.forms import CourseForm, LinkForm, InstructorForm, ReminderForm, NoteForm, FileForm, LoginForm, RegistrationForm

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

class HomeTestCase(TestCase):
    """Test the home view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()
        for i in range(12):
            reminder = Reminder.objects.create(user=user, name="Test", time=datetime.now())
            reminder.save()
        for i in range(12):
            course = Course.objects.create(user=user, title=f"TestCourse{i}")
            course.save()

    def test_home_renders(self):
        """Check the home renders"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("courses").count(), 4)
        self.assertEqual(response.context.get("reminders").count(), 4)
        self.assertTemplateUsed(response, "assistor/index.html")

class CoursesTestCase(TestCase):
    """Test the courses view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()
        for i in range(12):
            course = Course.objects.create(user=user, title=f"TestCourse{i}")
            course.save()

    def test_home_renders(self):
        """Check the home renders"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("courses"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("courses").count(), 12)
        self.assertTemplateUsed(response, "assistor/courses.html")

class CourseTestCase(TestCase):
    """Test the course view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()
        course = Course.objects.create(user=user, title="Test")
        course.save()
        for i in range(3):
            note = Note.objects.create(course=course, title=f"Test{1}", content="Lorem Ipsum....")
            note.save()
            instructor = Instructor.objects.create(course=course, title=["DR"], first_name=f"Test{i}", last_name=f"Test{i}", email=f"test{i}@test.com")
            instructor.save()
            link = Link.objects.create(course=course, name=f"TestLink{i}", url="https://hello.com")
            link.save()
        
    def test_course_renders(self):
        """Check the course renders"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Test")
        response = self.client.get(reverse("course", args=[course.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("notes").count(), 3)
        self.assertEqual(response.context.get("instructors").count(), 3)
        self.assertEqual(response.context.get("links").count(), 3)
        self.assertTemplateUsed(response, "assistor/course.html")

class NewCourseTestCase(TestCase):
    """Test the new course view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()

    def test_new_course_render(self):
        """Check the new course renders"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("course_new"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get("form"), CourseForm)
        self.assertTemplateUsed(response, "assistor/course_new.html")

    def test_new_course_is_created(self):
        """Check the new course is created"""
        self.client.login(username="admin", password="admin")
        response = self.client.post(reverse("course_new"), {
            "title": "Information Security", 
            "start_date": date(2022, 2, 28),
            "completion_date": date(2022, 7, 3),
            "grade": ["A"],
            "provider": "X University"
        })
        course = Course.objects.get(title="Information Security")
        self.assertRedirects(response, reverse("course", args=[course.id]))

class CourseTestCase(TestCase):
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
        self.assertEquals(response.status_code, 404)

class EditCourseTestCase(TestCase):
    """Test the edit course view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()
        course = Course.objects.create(user=user, title="Information Security")
        course.save()

    def test_edit_course_renders(self):
        """Check the edit course view renders"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Information Security")
        response = self.client.get(reverse("course_edit", args=[course.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("assistor/reminder_edit.html")

    def test_course_is_edited(self):
        """Check the course edit view edits course"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Information Security")

        response = self.client.post(reverse("course_edit", args=[course.id]), {
            "title": "Data Science",
            "start_date": date(2022, 7, 3),
            "provider": "University XYZ"
        })
        
        course = Course.objects.get(title="Data Science")
        self.assertEqual(course.title, "Data Science")
        self.assertRedirects(response, reverse("course", args=[course.id]))

class NotesTestCase(TestCase):
    """Test the notes view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()
        course = Course.objects.create(user=user, title="Information Security")
        course.save()
        for i in range(15):
            note = Note.objects.create(course=course, title=f"Test{i}", content=f"Lorem Ipsum{i}")
            note.save()

    def test_notes_render(self):
        """Check the notes render"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Information Security")
        response = self.client.get(reverse("notes", args=[course.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("notes").count(), 15)
        self.assertTemplateUsed(response, "assistor/notes.html")

class NoteTestCase(TestCase):
    """Test the note view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()
        course = Course.objects.create(user=user, title="Information Security")
        course.save()
        note = Note.objects.create(course=course, title="Lorem Ipsum", content="Lorem Ipsum sit amet........")
        note.save()

    def test_note_renders(self):
        """Check the note renders"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Information Security")
        note = Note.objects.get(title="Lorem Ipsum")
        response = self.client.get(reverse("note", args=[course.id, note.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("note"), note)
        self.assertTemplateUsed(response, "assistor/note.html")

class NewNoteTestCase(TestCase):
    """Test the new note view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        course = Course.objects.create(user=user, title="Information Security")
        user.save()
        course.save()

    def test_new_note_render(self):
        """Check the new note form renders"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Information Security")
        response = self.client.get(reverse("note_new", args=[course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("course"), course)
        self.assertIsInstance(response.context.get("form"), NoteForm)
        self.assertTemplateUsed(response, "assistor/note_new.html")

    def test_new_note_is_created(self):
        """Check the new note is created"""
        self.client.login(username="admin", password="admin")
        course = Course.objects.get(title="Information Security")
        response = self.client.post(reverse("note_new", args=[course.id]), {
            "title": "Lorem Ipsum",
            "content": "Lorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem IpsumLorem Ipsum"
        })
        note = Note.objects.get(title="Lorem Ipsum")
        self.assertRedirects(response, reverse("note", args=[course.id, note.id]))

class EditNoteTestCase(TestCase):
    """Test the edit note view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        course = Course.objects.create(user=user, title="Information Security")
        note = Note.objects.create(course=course, title="Lorem Ipsum", content="Lorem Ipsum sit amet........")
        note.save()
        user.save()
        course.save()

    def test_edit_note_renders(self):
        """Check the edit note view renders"""
        self.client.login(username="admin", password="admin")

        course = Course.objects.get(title="Information Security")
        note = Note.objects.get(title="Lorem Ipsum")

        response = self.client.get(reverse("note_edit", args=[course.id, note.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("course"), course)
        self.assertEqual(response.context.get("note"), note)
        self.assertTemplateUsed("assistor/note_edit.html")

    def test_note_is_edited(self):
        """Check the note edit view edits note"""
        self.client.login(username="admin", password="admin")
        
        course = Course.objects.get(title="Information Security")
        note = Note.objects.get(title="Lorem Ipsum")

        response = self.client.post(reverse("note_edit", args=[course.id, note.id]), {
                "title": "Lorem Ipsum Test Edit", 
                "content": "Lorem Ipsum Test Edit Content"
            })
        
        self.assertRedirects(response, reverse("note", args=[course.id, note.id]))

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

    def test_file_is_edited(self):
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

class RemindersTestCase(TestCase):
    """Test the reminders view"""
    def setUp(Self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()
        for i in range(12):
            reminder = Reminder.objects.create(user=user, name="Test", time=datetime.now())
            reminder.save()
    
    def test_reminders_renders(self):
        """Check the reminders view renders"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("reminders"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("reminders").count(), 12)
        self.assertTemplateUsed("assistor/reminders.html")

class NewReminderTestCase(TestCase):
    """Test the new reminder view"""
    def setUp(Self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()

    def test_new_reminder_renders(self):
        """Check the new reminder view renders"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("reminder_new"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get("form"), ReminderForm)
        self.assertTemplateUsed(response, "assistor/reminder_new.html")

    def test_new_reminder_is_created(self):
        """Check the new reminder is created"""
        self.client.login(username="admin", password="admin")
        response = self.client.post(reverse("reminder_new"), {
            "name": "Test",
            "time": datetime.now()
        })
        self.assertRedirects(response, reverse("index"))
        self.assertTrue(Reminder.objects.get(name="Test") != None)

class ReminderTestCase(TestCase):
    """Test the reminder view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()
        reminder = Reminder.objects.create(user=user, name="Test", time=datetime.now())
        reminder.save()

    def test_reminder_renders(self):
        """Check the reminder renders"""
        self.client.login(username="admin", password="admin")
        reminder = Reminder.objects.get(name="Test")
        response = self.client.get(reverse("reminder", args=[reminder.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("reminder"), reminder)
        self.assertTemplateUsed(response, "assistor/reminder.html")

class EditReminderTestCase(TestCase):
    """Test the edit reminder view"""
    def setUp(self):
        user = User.objects.create_user(first_name="admin", last_name="admin", username = "admin",
        email="admin@admin.com", password="admin")
        user.save()
        reminder = Reminder.objects.create(user=user, name="Test", time=datetime.now())
        reminder.save()

    def test_edit_reminder_renders(self):
        """Check the edit reminder view renders"""
        self.client.login(username="admin", password="admin")
        reminder = Reminder.objects.get(name="Test")
        response = self.client.get(reverse("reminder_edit", args=[reminder.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("assistor/reminder_edit.html")

    def test_reminder_is_edited(self):
        """Check the reminder edit view edits reminder"""
        self.client.login(username="admin", password="admin")
        reminder = Reminder.objects.get(name="Test")

        response = self.client.post(reverse("reminder_edit", args=[reminder.id]), {
            "name": "TestEdit", 
            "time": datetime.now()
        })
        
        self.assertRedirects(response, reverse("reminder", args=[reminder.id]))