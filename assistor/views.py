from cmath import log
from sys import excepthook
from django.http.response import Http404, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Course, Note, Reminder, User, File, Instructor, Link
from .forms import RegistrationForm, LoginForm, CourseForm, FileForm, NoteForm, NewReminderForm

# Create your views here.
@login_required(login_url="login")
def index(request):
    # Default page number
    return render(request, "assistor/index.html", {
        "courses": request.user.courses.all()[:4],
        "reminders": request.user.reminders.all()[:4]
    })


def login_view(request):
    """
    Display the login form :model:`assistor.User`.

    **Context**

    ``user``
        An instance of :model:`assistor.User`.

    **Template:**

    :template:`assistor/login.html`
    """
    
    # Process the submitted login form
    if request.method == "POST":
        form = LoginForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Attempt to sign user in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                form.add_error("username", "Invalid username and/or password.")
                return render(request, "assistor/login.html", {
                    "message": "Failed to login!",
                    "form": form
                })
        else:
            return render(request, "assistor/login.html", {
                "message": "Failed to login!",
                "form": form
            })

    # Show the login form
    elif request.method == "GET":
        return render(request, "assistor/login.html", {
            "form": LoginForm()
        })
    
    # Only POST and GET allowed
    else:
        return HttpResponseNotAllowed()


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    Display the registration form :model:`assistor.User`.

    **Context**

    ``user``
        An instance of :model:`assistor.User`.

    **Template:**

    :template:`assistor/register.html`
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        # Ensure the form data is valid
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                form.add_error("password", "Passwords must match.")
                return render(request, "assistor/register.html", {
                    "message": "Failed to register account!",
                    "form": form
                })

            # Attempt to create new user
            try:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError:
                return render(request, "assistor/register.html", {
                    "message": "Failed to register account!",
                    "form": form
                })
        else:
            return render(request, "assistor/register.html", {
                "form": form
            })
    
    # Request method is get
    elif request.method == "GET":
        form = RegistrationForm()
        return render(request, "assistor/register.html", {
            'form': form
        })
    
    # Only post and get methods are allowed
    else:
        return HttpResponseNotAllowed()

@login_required(login_url="login")
def new_course(request):
    form = CourseForm()

    # Add a new course
    if request.method == "POST":
        
        # Assign the form data from request
        course = Course(user=request.user)
        form = CourseForm(request.POST, instance=course)

        # Validate the form data
        if form.is_valid():

            # Course added successfully
            form.save()
            return HttpResponseRedirect(reverse("course", args=[course.id]))    

    # Show the form for adding course
    return render(request, "assistor/course_new.html", {
        "form": form
    })


@login_required(login_url="login")
def courses(request):
    """
    Display all courses of user
    """
    return render(request, "assistor/courses.html", {
        "courses": request.user.courses.all()
    })

@login_required(login_url="login")
def course(request, id):
    try:
        # Retreive course from database
        course = Course.objects.get(id=id)

        # Allow only the course creator to access
        if course.user == request.user:

            # Show the course
            return render(request, "assistor/course.html", {
                "course": course,
                "notes": Note.objects.filter(course=course)[:4],
                "files": File.objects.filter(course=course)[:4],
                "instructors": Instructor.objects.filter(course=course),
                "links": Link.objects.filter(course=course)
            })
        
        # Deny access to unauthorized user
        else:
            return HttpResponseForbidden()
    
    # Course with id does not exist
    except Course.DoesNotExist:
        return HttpResponseNotFound()

@login_required(login_url="login")
def course_edit(request, id):
    """
    Edit a course
    """
    form = CourseForm()
    
    # Edit a course
    if request.method == "POST":
        # Assign the form data from request
        try:
            course = Course.objects.get(id=id, user=request.user)
            form = CourseForm(request.POST, instance=course)

            # Validate the form data
            if form.is_valid():
                course.title = form.cleaned_data["title"]
                course.start_date = form.cleaned_data["start_date"]
                course.end_date = form.cleaned_data["completion_date"]
                course.grade = form.cleaned_data["grade"]
                course.provider = form.cleaned_data["provider"]

                # Save the edited course
                course.save()
                return HttpResponseRedirect(reverse("course", args=[course.id]))

        except Course.DoesNotExist:
            return HttpResponseNotFound()

    else:
        try:
            # Fill the form with course data
            course = Course.objects.get(id=id, user=request.user)
            form = CourseForm(instance=course)

            # Show the form for editing course
            return render(request, "assistor/course_edit.html", {
                "id": id,
                "form": form
            })

        except Course.DoesNotExist:
            return HttpResponseNotFound()

@login_required(login_url="login")
def notes(request, course_id):
    """
    Display all notes of the course
    """
    course = Course.objects.get(id=course_id)
    return render(request, "assistor/notes.html", {
        "course": course,
        "notes": course.notes.all()
    })

@login_required(login_url="login")
def note(request, course_id, note_id):
    try:
        # Retreive note and course from database
        course = Course.objects.get(id=course_id)
        note = Note.objects.get(id=note_id, course=course)

        # Allow only the note creator to access
        if note.course.user == request.user:
            
            # Show the note
            return render(request, "assistor/note.html", {
                "course" : Course.objects.get(id=course_id),
                "note" : note
            })

        # Deny access to unauthorized user
        else:
            return HttpResponseForbidden()

    # Note with note_id doesn't exist
    except (Note.DoesNotExist, Course.DoesNotExist):
        return HttpResponseNotFound()

@login_required(login_url="login")
def note_new(request, course_id):
    form = NoteForm()
    try:
        # Retreive course from database
        course = Course.objects.get(id = course_id)

        # Allow only the course creator to add and see note
        if course.user == request.user:

            # Add new Note
            if request.method == "POST":
                
                # Assign form data from post
                note = Note(course=course)
                form = NoteForm(request.POST, instance=note)

                # Validate form data
                if form.is_valid():
                    form.save()

                    # Show the note
                    return HttpResponseRedirect(reverse("note", args=[course_id, note.id]))
            
            # Show the form for adding new note
            return render(request, "assistor/note_new.html", {
                "course": course,
                "form": form
            })
        
        # Deny access to unauthorized user
        else:
            return HttpResponseForbidden()
    
    # Course doesn't exist in database
    except Course.DoesNotExist:
        return HttpResponseNotFound()

@login_required(login_url="login")
def note_edit(request, course_id, note_id):
    """
    Edit a note
    """ 
    if request.method == "POST":
        try:
            course = Course.objects.get(id=course_id)
            note = Note.objects.get(id=note_id)

            # Prevent unauthorised user from accessing note editing form
            if request.user == course.user:
                form = NoteForm(request.POST, instance=note)
                if form.is_valid():
                    note.title = form.cleaned_data["title"]
                    note.content = form.cleaned_data["content"]
                    note.save()
                    return HttpResponseRedirect(reverse("note", args=[course.id, note.id]))
                else:
                    form = NoteForm(instance=note)
                    return render(request, "assistor/note_edit.html", {
                        "course": course,
                        "note": note,
                        "form": form
                    })
            else:
                return HttpResponseForbidden()

        except (Course.DoesNotExist, Note.DoesNotExist):
            return HttpResponseNotFound()

    else:
        try:
            course = Course.objects.get(id=course_id)
            note = Note.objects.get(id=note_id)

            # Prevent unauthorised user from accessing note editing form
            if request.user == course.user:
                form = NoteForm(instance=note)
                return render(request, "assistor/note_edit.html", {
                    "course": course,
                    "note": note,
                    "form": form
                })

            else:
                return HttpResponseForbidden()

        except (Course.DoesNotExist, Note.DoesNotExist):
            return HttpResponseNotFound()


@login_required(login_url="login")
def files(request, course_id):
    """
    Show all files of a course
    """
    course = Course.objects.get(id=course_id)
    return render(request, "assistor/files.html", {
        "course": course,
        "files": File.objects.filter(course=course)
    })

@login_required(login_url="login")
def file(request, course_id, file_id):
    """
    Show a file
    """
    try:
        return render(request, 'assistor/file.html', {
            "course": Course.objects.get(id=course_id),
            "file": File.objects.get(id=file_id)
        })
    except (Course.DoesNotExist, File.DoesNotExist):
        return HttpResponseNotFound()

@login_required(login_url="login")
def course_delete(request, id):
    # Retreive course from database
    course = Course.objects.get(id=id)

    # Allow only the course creator to delete
    if request.user == course.user:
        
        # Delete the course
        course.delete()

        return HttpResponseRedirect(reverse("index"))

    # Deny access to unauthorized users
    else:
        return HttpResponseForbidden()

@login_required(login_url="login")
def new_reminder(request):
    form = NewReminderForm()

    # Add a new reminder
    if request.method == "POST":

        # Assign the form data from post
        reminder = Reminder(user=request.user)
        form = NewReminderForm(request.POST, instance=reminder)

        # Validate the form data
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))

    # Show form for adding new reminder
    return render(request, "assistor/reminder_new.html", {
        "form": form
    })

@login_required(login_url="login")
def reminder_delete(request, id):
    # Retreive reminder from database
    reminder = Reminder.objects.get(id=id)

    # Allow only the reminder creator to delete
    if request.user == reminder.user:
        
        # Delete the reminder
        reminder.delete()

        return HttpResponseRedirect(reverse("index"))

    # Deny unauthorized users
    else:
        return HttpResponseForbidden()


@login_required(login_url="login")
def note_delete(request, course_id, note_id):
    try:
        # Retreive note from database
        note = Note.objects.get(id=note_id)

        # Allow only the note creator to delete
        if request.user == note.course.user:
            
            # Delete the note
            note.delete()

            return HttpResponseRedirect(reverse("course", args=[course_id]))
            
        # Deny access to unauthorized user
        else:
            return HttpResponseForbidden()

    # Note doesn't exist in the database
    except Note.DoesNotExist:
        return HttpResponseNotFound()

@login_required(login_url="login")
def new_file(request, course_id):
    """
    Display the file form :model:`assistor.File`.

    **Context**

    ``course``
        An instance of :model:`assistor.course`.

    ``form``
        An instance of :form:`assistor.FileForm`.
        
    **Template:**

    :template:`assistor/file_new.html`
    """
    try:
        form = FileForm()

        # Retreive course from database
        course = Course.objects.get(id=course_id)

        # Add the new file
        if request.method == "POST":

            # Assign form data from post
            file = File(course=course)
            form = FileForm(request.POST, request.FILES, instance=file)

            # Validate the form data
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("course", args=[course.id]))
            else:
                return render(request, "assistor/file_new.html", {
                "message": "Failed to add file!",
                "course": course,
                "form": form
            })

        # Show the New File Form
        elif request.method == "GET":
            return render(request, "assistor/file_new.html", {
                "course": course,
                "form": form
            })

        # Only POST and GET allowed
        else:
            return HttpResponseNotAllowed()    
            
    # Course doesn't exist in database
    except Course.DoesNotExist:
        return HttpResponseNotFound()

@login_required(login_url="login")
def file_delete(request, course_id, file_id):
    try:
        # Retreive file from the database
        file = File.objects.get(id=file_id)

        # Allow only the file owner to delete
        if request.user == file.course.user:
            
            # Delete the file
            file.delete()

            return HttpResponseRedirect(reverse("course", args=[course_id]))

        # Deny access to unauthorized users
        else:
            return HttpResponseForbidden()


    # File doesn't exist in the database
    except File.DoesNotExist:
        return HttpResponseNotFound()
