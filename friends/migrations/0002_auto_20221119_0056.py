# Generated by Django 3.2.7 on 2022-11-18 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='friendlist',
            options={'ordering': ['-created_at', '-pk']},
        ),
        migrations.AlterModelOptions(
            name='friendrequest',
            options={'ordering': ['-created_at', '-pk']},
        ),
    ]