from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("reminders/new", views.new_reminder, name="reminder_new"),
    path("reminders/<int:id>/delete", views.reminder_delete, name="reminder_delete"),
    path("courses/new", views.new_course, name="course_new"),
    path("courses/<int:id>", views.course, name="course"),
    path("courses/<int:id>/delete", views.course_delete, name="course_delete"),
    path("courses/<int:course_id>/notes/<int:note_id>", views.note, name="note"),
    path("courses/<int:course_id>/notes/new", views.new_note, name="note_new"),
    path("courses/<int:course_id>/notes/<int:note_id>/delete", views.note_delete, name="note_delete"),
    path("courses/<int:course_id>/files/new", views.new_file, name="file_new"),
    path("courses/<int:course_id>/files/<int:file_id>/delete", views.file_delete, name="file_delete")
]