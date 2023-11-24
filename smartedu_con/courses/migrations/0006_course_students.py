# Generated by Django 4.1.3 on 2023-11-23 21:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0005_course_teacher"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="students",
            field=models.ManyToManyField(
                blank=True, related_name="joined_courses", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
