from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("courses", views.courses, name="courses"),
    path("courses/<int:id>", views.course, name="course"),
    path("courses/<int:id>/edit", views.course_edit, name="course_edit"),
    path("courses/new", views.new_course, name="course_new"),
    path("courses/<int:id>/delete", views.course_delete, name="course_delete"),
    path("courses/<int:course_id>/notes", views.notes, name="notes"),
    path("courses/<int:course_id>/notes/<int:note_id>", views.note, name="note"),
    path("courses/<int:course_id>/notes/new", views.note_new, name="note_new"),
    path("courses/<int:course_id>/notes/<int:note_id>/edit", views.note_edit, name="note_edit"),
    path("courses/<int:course_id>/notes/<int:note_id>/delete", views.note_delete, name="note_delete"),
    path("courses/<int:course_id>/files", views.files, name="files"),
    path("courses/<int:course_id>/files/new", views.new_file, name="file_new"),
    path("courses/<int:course_id>/files/<int:file_id>", views.file, name="file"),
    path("courses/<int:course_id>/files/<int:file_id>/edit", views.file_edit, name="file_edit"),
    path("courses/<int:course_id>/files/<int:file_id>/delete", views.file_delete, name="file_delete"),
    path("reminders/new", views.new_reminder, name="reminder_new"),
    path("reminders/<int:id>/delete", views.reminder_delete, name="reminder_delete")
]