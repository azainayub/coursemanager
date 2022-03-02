from django.http.response import Http404, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Course, Note, Reminder, User, File, Instructor, Link
from .forms import RegistrationForm, LoginForm, CourseForm, NewFileForm, NewNoteForm, NewReminderForm

# Create your views here.
@login_required(login_url="login")
def index(request):
    # Default page number
    return render(request, "assistor/index.html", {
        "courses": request.user.courses.all()[:4],
        "reminders": request.user.reminders.all()[:4]
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            form = LoginForm(request.POST)
            form.add_error("username", "Invalid username and/or password.")
            return render(request, "assistor/login.html", {
                "form": form
            })
    else:
        form = LoginForm()
        return render(request, "assistor/login.html", {
            "form": form
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            form.add_error("password", "Passwords must match.")
            return render(request, "assistor/register.html", {
                "form": form
            })

        # Attempt to create new user
        try:
            if form.is_valid():
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
            else:
                return render(request, "assistor/register.html", {
                "form": form
            })
        except IntegrityError:
            return render(request, "assistor/register.html", {
                "form": form
            }) 
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        form = RegistrationForm()
        return render(request, "assistor/register.html", {
            'form': form
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
def note(request, course_id, note_id):
    try:
        # Retreive note from database
        note = Note.objects.get(id=note_id)

        # Allow only the note creator to access
        if note.course.user == request.user:
            
            # Show the note
            return render(request, "assistor/note.html", {
                "note" : note
            })

        # Deny access to unauthorized user
        else:
            return HttpResponseForbidden()

    # Note with note_id doesn't exist
    except Note.DoesNotExist:
        return HttpResponseNotFound()


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
def new_note(request, course_id):
    form = NewNoteForm()
    try:
        # Retreive course from database
        course = Course.objects.get(id = course_id)

        # Allow only the course creator to add and see note
        if course.user == request.user:

            # Add new Note
            if request.method == "POST":
                
                # Assign form data from post
                note = Note(course=course)
                form = NewNoteForm(request.POST, instance=note)

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
    try:
        form = NewFileForm()

        # Retreive course from database
        course = Course(id = course_id)
        
        # Add new file
        if request.method == "POST":

            # Assign form data from post
            file = File(course=course)
            form = NewFileForm(request.POST, request.FILES, instance=file)

            # Validate the form data
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("course", args=[course.id]))
            
        # Show form for adding a new file
        return render(request, "assistor/file_new.html", {
            "course": course,
            "form": form
        })

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
