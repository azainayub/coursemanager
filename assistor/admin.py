from django.contrib import admin
from .models import File, Reminder, User, Course, Note, Instructor, Link

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Note)
admin.site.register(Reminder)
admin.site.register(File)
admin.site.register(Instructor)
admin.site.register(Link)