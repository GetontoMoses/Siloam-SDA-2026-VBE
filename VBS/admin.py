from django.contrib import admin

from VBS.models import Attendance, Child, Guardian, Station, Teacher

# Register your models here.
admin.site.register(Guardian)
admin.site.register(Child)
admin.site.register(Attendance)
admin.site.register(Teacher)
admin.site.register(Station)
