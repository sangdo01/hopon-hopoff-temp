# Generated by Django 5.1.7 on 2025-04-17 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_alter_profile_options_alter_userrole_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
