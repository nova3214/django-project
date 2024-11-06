from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'submitted_at')
    list_filter = ('submitted_at',)