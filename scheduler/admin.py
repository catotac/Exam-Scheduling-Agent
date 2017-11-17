from django.contrib import admin

from .models import *

# Register models to admin site
admin.site.register(Course)
admin.site.register(Building)
admin.site.register(Exam)
admin.site.register(Classroom)
admin.site.register(ClassroomSchedule)
admin.site.register(TA)
admin.site.register(TASchedule)
admin.site.register(TAExam)
admin.site.register(TACourse)
