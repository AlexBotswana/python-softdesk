# Generated by Django 4.2.7 on 2024-02-14 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('softdeskapi', '0006_rename_birth_day_user_birthdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500, unique=True)),
                ('blacklisted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
