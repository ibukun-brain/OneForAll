# Generated by Django 3.2.7 on 2022-11-19 19:44

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_customuser_cover_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='mobile_no',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default="+2348052940205", max_length=128, region=None),
            preserve_default=False,
        ),
    ]
