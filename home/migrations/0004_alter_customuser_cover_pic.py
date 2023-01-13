# Generated by Django 3.2.7 on 2022-11-01 13:15

from django.db import migrations, models
import ofa.utils.media


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_customuser_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cover_pic',
            field=models.ImageField(blank=True, default=ofa.utils.media.default_cover_image, null=True, upload_to=ofa.utils.media.cover_image_upload_path, verbose_name='Cover Picture'),
        ),
    ]
