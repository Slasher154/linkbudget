__author__ = 'thanatv'

from django.contrib import admin
from mysite.models import Parent, Child, Progress
from linkbudget.models import UplinkBeam, UplinkDefinedContour


class ProgressAdmin(admin.ModelAdmin):
    pass


class UplinkDefinedContourInline(admin.TabularInline):
    model = UplinkDefinedContour


class UplinkBeamAdmin(admin.ModelAdmin):
    inlines = [
        UplinkDefinedContourInline,
    ]


admin.site.register(Progress, ProgressAdmin)
admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(UplinkBeam, UplinkBeamAdmin)
admin.site.register(UplinkDefinedContour)