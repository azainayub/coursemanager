from django.http.response import Http404, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Course, Note, Reminder, User, File
from .forms import NewCourseForm, NewFileForm, NewNoteForm, NewReminderForm

# Create your views here.
@login_required(login_url="login")
def index(request):
    # Default page number
    return render(request, "assistor/index.html", {
        "courses": request.user.courses.all(),
        "reminders": request.user.reminders.all()
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
            return render(request, "assistor/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "assistor/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "assistor/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "assistor/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "assistor/register.html")

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
                "notes": Note.objects.filter(course=course),
                "files": File.objects.filter(course=course)
            })
        
        # Deny access to unauthorized user
        else:
            return HttpResponseForbidden()
    
    # Course with id does not exist
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
    form = NewCourseForm()

    # Add a new course
    if request.method == "POST":
        
        # Assign the form data from request
        course = Course(user=request.user)
        form = NewCourseForm(request.POST, instance=course)

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
