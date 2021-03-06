from django.http.response import HttpResponseNotAllowed, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Course, Note, Reminder, User, File, Instructor, Link
from .forms import (
    RegistrationForm,
    LoginForm,
    CourseForm,
    FileForm,
    NoteForm,
    LinkForm,
    InstructorForm,
    ReminderForm,
)


# Create your views here.
@login_required(login_url="login")
def index(request):
    """
    Display the Home Page :model:`assistor.Course`.

    **Context**

    ``courses``
        An instance of :models:`assistor.Course`.

    ``reminders``
        An instance of :models:`assistor.Reminders`.

    **Template:**

    :template:`assistor/index.html`
    """
    return render(
        request,
        "assistor/index.html",
        {
            "courses": request.user.courses.all()[:4],
            "reminders": request.user.reminders.all()[:4],
            "course_form": CourseForm(),
            "reminder_form": ReminderForm(),
        },
    )


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
                return render(
                    request,
                    "assistor/login.html",
                    {"message": "Failed to login!", "form": form},
                )
        else:
            return render(
                request,
                "assistor/login.html",
                {"message": "Failed to login!", "form": form},
            )

    # Show the login form
    elif request.method == "GET":
        return render(request, "assistor/login.html", {"form": LoginForm()})

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
            password = form.cleaned_data["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                form.add_error("password", "Passwords must match.")
                return render(
                    request,
                    "assistor/register.html",
                    {"message": "Failed to register account!", "form": form},
                )

            # Attempt to create new user
            try:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                )
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError:
                return render(
                    request,
                    "assistor/register.html",
                    {"message": "Failed to register account!", "form": form},
                )
        else:
            return render(request, "assistor/register.html", {"form": form})

    # Request method is get
    elif request.method == "GET":
        form = RegistrationForm()
        return render(request, "assistor/register.html", {"form": form})

    # Only post and get methods are allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def courses(request):
    """
    Display all courses of user
    """
    return render(
        request,
        "assistor/courses.html",
        {
            "courses": request.user.courses.all(),
            "course_form": CourseForm(),
        },
    )


@login_required(login_url="login")
def course(request, course_id):
    """
    Display the course :model:`assistor.Course`.

    **Context**

    ``course``
        An instance of :model:`assistor.Course`.

    ``notes``
        An instance of :model:`assistor.Notes`.

    ``files``
        An instance of :model:`assistor.File`.

    ``instructors``
    An instance of :model:`assistor.Instructor`.

    ``links``
    An instance of :model:`assistor.Link`.

    **Template:**

    :template:`assistor/course.html`
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)

    # Show the course
    return render(
        request,
        "assistor/course.html",
        {
            "course": course,
            "notes": Note.objects.filter(course=course)[:4],
            "files": File.objects.filter(course=course)[:4],
            "instructors": Instructor.objects.filter(course=course),
            "links": Link.objects.filter(course=course),
            "course_form": CourseForm(instance=course),
            "note_form": NoteForm(),
            "file_form": FileForm(),
            "instructor_form": InstructorForm(),
            "link_form": LinkForm(),
        },
    )


@login_required(login_url="login")
def notes(request, course_id):
    """
    Display the notes :model:`assistor.Note`.

    **Context**

    ``course``
        An instance of :model:`assistor.Course`.

    ``course``
        An instance of :model:`assistor.Note`.

    **Template:**

    :template:`assistor/notes.html`
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)
    return render(
        request,
        "assistor/notes.html",
        {
            "course": course,
            "notes": course.notes.all(),
            "course_form": CourseForm(instance=course),
            "note_form": NoteForm(),
        },
    )


@login_required(login_url="login")
def note(request, course_id, note_id):
    """
    Display a note :model:`assistor.Note`.

    **Context**

    ``course``
        An instance of :model:`assistor.Course`.

    ``note``
        An instance of :form:`assistor.Note`.

    **Template:**

    :template:`assistor/note.html`
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)
    note = get_object_or_404(Note, id=note_id, course=course)

    # Show the note
    return render(
        request,
        "assistor/note.html",
        {
            "course": course,
            "note": note,
            "course_form": CourseForm(instance=course),
            "note_form": NoteForm(),
            "note_edit_form": NoteForm(instance=note),
        },
    )


@login_required(login_url="login")
def files(request, course_id):
    """
    Display the files :model:`assistor.File`.

    **Context**

    ``course``
        An instance of :model:`assistor.Course`.

    ``files``
        An instance of :model:`assistor.File`.

    **Template:**

    :template:`assistor/files.html`
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)
    return render(
        request,
        "assistor/files.html",
        {
            "course": course,
            "files": File.objects.filter(course=course),
            "course_form": CourseForm(instance=course),
            "file_form": FileForm(),
        },
    )


@login_required(login_url="login")
def file(request, course_id, file_id):
    """
    Display a file :model:`assistor.File`.

    **Context**

    ``course``
        An instance of :model:`assistor.Course`.

    ``files``
        An instance of :model:`assistor.File`.

    **Template:**

    :template:`assistor/files.html`
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)
    file = get_object_or_404(File, id=file_id, course=course)

    return render(request, "assistor/file.html", {
        "course": course, 
        "file": file, 
        "file_form": FileForm(),
        "file_edit_form": FileForm(instance=file),
        "course_form": CourseForm(instance=course),
    })


@login_required(login_url="login")
def reminder(request, reminder_id):
    """
    Display the reminder :model:`assistor.Reminder`.

    **Context**

    ``reminder``
        An instance of :model:`assistor.Reminder`.

    **Template:**

    :template:`assistor/reminder.html`
    """
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    return render(request, "assistor/reminder.html", {
        "reminder": reminder, 
        "reminder_form": ReminderForm(),
        "reminder_edit_form": ReminderForm(instance=reminder),
    })


@login_required(login_url="login")
def reminders(request):
    """
    Display the reminders :model:`assistor.Reminder`.

    **Context**

    ``courses``
        An instance of :Objects:`assistor.Course`.

    **Template:**

    :template:`assistor/reminders.html`
    """
    return render(
        request, "assistor/reminders.html", {"reminders": request.user.reminders.all(), "reminder_form": ReminderForm(),}
    )


@login_required(login_url="login")
def course_new(request):
    """
    Add a new course

    """

    # Add a new course
    if request.method == "POST":

        # Assign the form data from request
        course = Course(user=request.user)
        form = CourseForm(request.POST, instance=course)

        # Validate the form data
        if form.is_valid():

            # Course added successfully
            form.save()
            return JsonResponse(course.serialize(), status=201, safe=False)

        # Data is invalid
        else:
            return JsonResponse(form.errors, status=400, safe=False)

    # Only POST allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def course_edit(request, course_id):
    """
    Display the course edit form :model:`assistor.Course`.

    **Context**

    ``form``
        An instance of :form:`assistor.CourseForm`.

    **Template:**

    :template:`assistor/course_edit.html`
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)

    # Edit a course
    if request.method == "POST":

        form = CourseForm(request.POST, instance=course)

        # Validate the form data
        if form.is_valid():
            course.title = form.cleaned_data["title"]
            course.start_date = form.cleaned_data["start_date"]
            course.completion_date = form.cleaned_data["completion_date"]
            course.grade = form.cleaned_data["grade"]
            course.provider = form.cleaned_data["provider"]

            # Save the edited course
            course.save()
            return JsonResponse(course.serialize(), status=201, safe=False)
        else:
            return JsonResponse(form.errors, status=400, safe=False)
    
    # Only POST allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def course_delete(request, course_id):
    """
    Delete the course :model:`assistor.Course`.
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)

    # Delete the course
    course.delete()

    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def note_new(request, course_id):
    """
    Add a new note
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)
    # Retreive course from database
    course = Course.objects.get(id=course_id)

    # Add new Note
    if request.method == "POST":

        # Assign form data from post
        note = Note(course=course)
        form = NoteForm(request.POST, instance=note)

        # Validate form data
        if form.is_valid():
            form.save()

            # Show the note
            return JsonResponse(note.serialize(), status=201, safe=False)
        else:
            return JsonResponse(form.errors, status=400, safe=False)

    # Only GET and POST allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def note_edit(request, course_id, note_id):
    """
    Display a edit note form :model:`assistor.Note`.

    **Context**

    ``course``
        An instance of :model:`assistor.Course`.

    ``form``
        An instance of :form:`assistor.NoteForm`.

    **Template:**

    :template:`assistor/note_edit.html`
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)
    note = get_object_or_404(Note, id=note_id, course=course)

    # Edit the note
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note.title = form.cleaned_data["title"]
            note.content = form.cleaned_data["content"]
            note.save()
            return JsonResponse(note.serialize(), status=201, safe=False)
        else:
            return JsonResponse(form.errors, status=400, safe=False)

    # Only POST allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def note_delete(request, course_id, note_id):
    """
    Delete the note :model:`assistor.Note`.
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)
    note = get_object_or_404(Note, id=note_id, course=course)

    # Delete the note
    note.delete()

    return HttpResponseRedirect(reverse("course", args=[course_id]))


@login_required(login_url="login")
def reminder_new(request):
    """
    Display the reminder form :model:`assistor.Reminder`.

    **Context**

    ``form``
        An instance of :form:`assistor.ReminderForm`.

    **Template:**

    :template:`assistor/reminder_new.html`
    """
    # Add a new reminder
    if request.method == "POST":

        # Assign the form data from post
        reminder = Reminder(user=request.user)
        form = ReminderForm(request.POST, instance=reminder)

        # Validate the form data
        if form.is_valid():
            form.save()
            return JsonResponse(reminder.serialize(), status=201, safe=False)
        else:
            return JsonResponse(form.errors, status=400, safe=False)

    # Only GET and POST allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def reminder_edit(request, reminder_id):
    """
    Edit a Reminder
    """

    # Retrieve object
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)

    # Edit the reminder
    if request.method == "POST":
        form = ReminderForm(request.POST, instance=reminder)

        if form.is_valid():
            reminder.name = form.cleaned_data["name"]
            reminder.time = form.cleaned_data["time"]
            reminder.save()
            return JsonResponse(reminder.serialize(), status=201, safe=False)
        else:
            return JsonResponse(form.errors, status=400, safe=False)

    # Only POST allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def reminder_delete(request, reminder_id):
    """
    Delete the reminder :model:`assistor.Reminder`.
    """
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)

    # Delete the reminder
    reminder.delete()

    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def file_new(request, course_id):
    """
    Add a new file
    """
    # Retreive course from database
    course = get_object_or_404(Course, id=course_id, user=request.user)

    # Add the new file
    if request.method == "POST":

        # Assign form data from post
        file = File(course=course)
        form = FileForm(request.POST, request.FILES, instance=file)

        # Validate the form data
        if form.is_valid():
            form.save()
            return JsonResponse(file.serialize(), status=201, safe=False)
        else:
            return JsonResponse(form.errors, status=400, safe=False)

    # Only POST allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def file_edit(request, course_id, file_id):
    """
    Edit the File
    """

    # Retrieve objects
    course = get_object_or_404(Course, id=course_id, user=request.user)
    file = get_object_or_404(File, id=file_id, course=course)

    # Edit the file
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES, instance=file)

        if form.is_valid():
            file.name = form.cleaned_data["name"]
            file.category = form.cleaned_data["category"]
            file.file = form.cleaned_data["file"]
            file.save()
            return JsonResponse(file.serialize(), status=201, safe=False)
        else:
            return JsonResponse(form.errors, status=400, safe=False)
 
    # Only POST allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def file_delete(request, course_id, file_id):
    """
    Delete the file :model:`assistor.File`.
    """
    course = get_object_or_404(Course, id=course_id, user=request.user)
    file = get_object_or_404(File, id=file_id, course=course)

    # Delete the file
    file.delete()

    return HttpResponseRedirect(reverse("course", args=[course_id]))


@login_required(login_url="login")
def link_new(request, course_id):
    """
    Add a new Link
    """

    course = get_object_or_404(Course, id=course_id, user=request.user)
    link = Link(course=course)

    # Add a new link
    if request.method == "POST":
        form = LinkForm(request.POST, instance=link)

        # Check form is valid
        if form.is_valid():
            form.save()
            return JsonResponse(link.serialize(), status=201, safe=False)

        else:
            return JsonResponse(form.errors, status=400, safe=False)

    # Only POST allowed
    else:
        return HttpResponseNotAllowed()


@login_required(login_url="login")
def instructor_new(request, course_id):
    """
    Add new Instructor
    """

    course = get_object_or_404(Course, id=course_id, user=request.user)
    instructor = Instructor(course=course)

    # Add a new instructor
    if request.method == "POST":
        form = InstructorForm(request.POST, instance=instructor)

        # Check form is valid
        if form.is_valid():
            form.save()
            return JsonResponse(instructor.serialize(), status=201 ,safe=False)

        else:
            return JsonResponse(form.errors, status=400 ,safe=False)

    # Only POST allowed
    else:
        return HttpResponseNotAllowed()
