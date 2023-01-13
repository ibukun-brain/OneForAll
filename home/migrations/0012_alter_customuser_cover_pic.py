# Generated by Django 3.2.7 on 2022-11-16 20:29

from django.db import migrations, models
import ofa.utils.media


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_customuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cover_pic',
            field=models.ImageField(blank=True, null=True, upload_to=ofa.utils.media.cover_image_upload_path, verbose_name='Cover Picture'),
        ),
    ]