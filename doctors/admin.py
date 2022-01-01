from django.contrib import admin

from .models import Doctor, Specialty

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Specialty)
