# Generated by Django 5.1 on 2024-08-28 17:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="linkaudit",
            old_name="count",
            new_name="hits",
        ),
    ]
