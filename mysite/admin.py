__author__ = 'thanatv'

from django.contrib import admin
from models import Progress


class ProgressAdmin(admin.ModelAdmin):
    pass

admin.site.register(Progress, ProgressAdmin)