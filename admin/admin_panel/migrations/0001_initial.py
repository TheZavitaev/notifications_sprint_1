# Generated by Django 4.0 on 2022-01-17 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Наименование')),
                ('code', models.CharField(choices=[('welcome_letter', 'Приветственное письмо'), ('selection_movies', 'Подборка фильмов'), ('personal_newsletter', 'Персональная рассылка фильмов'), ('mailing_weekly', 'Еженедельная рассылка'), ('mailing_monthly', 'Ежемесячная рассылка'), ('security_notification', 'Уведомление системы безопасности')], max_length=50)),
                ('template', models.TextField()),
                ('subject', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
            ],
            options={
                'db_table': 'notification_templates',
            },
        ),
        migrations.CreateModel(
            name='MailingTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'В очередь на отправку'), ('in_process', 'В процессе отправки'), ('done', 'Отправлено'), ('cancelled', 'Отменено')], default='pending', max_length=250)),
                ('is_promo', models.BooleanField(default=True)),
                ('priority', models.CharField(choices=[('high', 'Высокий приоритет'), ('medium', 'Средний приоритет'), ('low', 'Низкий приоритет')], default='low', max_length=250)),
                ('context', models.JSONField(default={})),
                ('scheduled_datetime', models.DateTimeField(blank=True, null=True)),
                ('execution_datetime', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.template')),
            ],
            options={
                'db_table': 'mailing_tasks',
            },
        ),
    ]
