from enum import Enum

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class TemplateCodes(models.TextChoices):
    """Email template codes."""

    welcome_letter = 'welcome_letter', 'Приветственное письмо'
    selection_movies = 'selection_movies', 'Подборка фильмов'
    personal_newsletter = 'personal_newsletter', 'Персональная рассылка фильмов'

    mailing_weekly = 'mailing_weekly', 'Еженедельная рассылка'
    mailing_monthly = 'mailing_monthly', 'Ежемесячная рассылка'


class Template(models.Model):
    """Email template."""

    title = models.CharField('Наименование', max_length=250)
    code = models.CharField(choices=TemplateCodes.choices, max_length=50)
    html = models.TextField()
    subject = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """Save template."""

        if not self.id:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'email_templates'


class TransportType(str, Enum):
    email = 'email'
    sms = 'sms'


class NotificationStatuses(str, Enum):
    to_send = 'pending'
    in_process = 'in_process'
    done = 'done'
    cancelled = 'cancelled'


class Priority(str, Enum):
    high = 'high'
    medium = 'medium'
    low = 'low'


class MailingTask(models.Model):
    """Model mailing task."""

    NOTIFICATION_STATUSES = (
        (NotificationStatuses.to_send, 'pending'),
        (NotificationStatuses.in_process, 'in_process'),
        (NotificationStatuses.done, 'done'),
        (NotificationStatuses.cancelled, 'cancelled'),
    )
    status = models.CharField(
        max_length=250,
        choices=NOTIFICATION_STATUSES,
        default=NotificationStatuses.to_send,
    )
    PRIORITY_QUEUE = (
        (Priority.high, 'High'),
        (Priority.medium, 'Medium'),
        (Priority.low, 'Low')
    )

    priority = models.CharField(
        max_length=250,
        choices=PRIORITY_QUEUE,
        default=Priority.low
    )

    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    template_data = JSONField(default={})

    scheduled_datetime = models.DateTimeField(blank=True, null=True)
    execution_datetime = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """Save task."""

        if not self.id:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'mailing_tasks'
