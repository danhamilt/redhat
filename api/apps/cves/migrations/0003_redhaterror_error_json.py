# Generated by Django 4.2.6 on 2023-10-25 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cves', '0002_alter_redhaterror_error_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='redhaterror',
            name='error_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
