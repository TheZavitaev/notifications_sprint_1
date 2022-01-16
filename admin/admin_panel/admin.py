from django.contrib import admin

from admin.admin_panel.models import Template, MailingTask


@admin.register(Template)
class TemplatesAdmin(admin.ModelAdmin):
    """Admin interface for Template."""


@admin.register(MailingTask)
class TasksAdmin(admin.ModelAdmin):
    """Admin interface for Task."""
