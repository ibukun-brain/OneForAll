import auto_prefetch

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import timesince
from django.utils.dateformat import format as date_fmt

from ofa.utils.choices import Gender, Status
from ofa.utils.managers import CustomUserManager
from ofa.utils.models import NamedTimeBasedModel
from ofa.utils.media import ( 
    image_upload_path, default_cover_image, 
    cover_image_upload_path
)
from ofa.utils.managers import CustomUserManager
from ofa.utils.html import (
    image_to_html, image_to_html_profile,
    image_to_html_small, image_to_html_edit 
)
from ofa.utils.validators import validate_age
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CustomUser(AbstractUser):
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    slug = models.SlugField(blank=True, unique=True)
    additional_name = models.CharField(max_length=100, blank=True)
    overview = models.TextField(max_length=300, null=True, blank=True)
    email = models.EmailField(verbose_name="email address", unique=True)
    # mobile_no = models.CharField(max_length=20, null=True, blank=True)
    mobile_no = PhoneNumberField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = auto_prefetch.ForeignKey(
        "location.Country", on_delete=models.SET_NULL, null=True, blank=True
    )
    city = models.CharField(max_length=200, blank=True, help_text="Lives in")
    gender = models.CharField(
        max_length=15, choices=Gender.choices
    )
    profile_pic = models.ImageField(
        upload_to=image_upload_path,
        blank=True,
        verbose_name="Profile Picture",
        null=True,
    )
    cover_pic =  models.ImageField(
        upload_to=cover_image_upload_path,
        blank=True,
        verbose_name="Cover Picture",
        null=True,
        default=default_cover_image
    )
    occupation = models.CharField(max_length=50, blank=True)
    allowed = models.BooleanField(help_text="Allow anyone to add you to their team / group", default=True)
    status = models.CharField(max_length=50, choices=Status.choices)
    is_verified = models.BooleanField(default=False)
    objects = CustomUserManager()


    def __str__(self):
        return self.get_full_name() or self.email

    @property
    def image_url(self):

        if self.profile_pic:
            return self.profile_pic.url

        return f"{settings.MEDIA_URL}/default/placeholder.jpg"

    @property
    def profile_image(self):

        """
        renders a html img tag with our profile pic 
        or return default jdenticon
        """
        if self.profile_pic:
            return image_to_html(self.profile_pic.url, self.username)

        return image_to_html(image=None, username=self.username)

    @property
    def profile_image_sm(self):

        if self.profile_pic:
            return image_to_html_small(self.profile_pic.url, self.username)

        return image_to_html_small(image=None, username=self.username)

    @property
    def profile_image_edit(self):

        if self.profile_pic:
            return image_to_html_edit(self.profile_pic.url, self.username)

        return image_to_html_edit(image=None, username=self.username)

    

    @property
    def profile_image_lg(self):

        if self.profile_pic:
            return image_to_html_profile(self.profile_pic.url, self.username)

        return image_to_html_profile(image=None, username=self.username)
    
    @property
    def cover_image_url(self):

        if self.cover_pic:
            return self.cover_pic.url

        return f"{settings.MEDIA_URL}/default/cover-default.jpg"



class Education(NamedTimeBasedModel):
    user= auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE
    )
    university_logo = models.URLField(
                blank=True, 
                help_text="Provide an image address to the company logo"
            )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} -> {self.start_date} - {self.end_date}"

    @property
    def date_range(self):
        """
        Properly formatted date range for rendering education section
        """
        start_date = date_fmt(self.start_date, "M Y")

        if self.end_date:
            end_date = date_fmt(self.end_date, "M Y")
        else:
            end_date = "present"

        return f"{start_date} - {end_date}" 


class WorkPlace(NamedTimeBasedModel):
    user = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE
    )
    company_logo = models.URLField(
            blank=True, 
            help_text="Provide an image address to the company logo"
        )
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    @property
    def duration(self):
        return timesince(self.start_date, self.end_date)

    @property
    def date_range(self):
        """
        Properly formatted date range for rendering education section
        """
        start_date = date_fmt(self.start_date, "M Y")

        if self.end_date:
            end_date = date_fmt(self.end_date, "M Y")
        else:
            end_date = "present"

        return f"{start_date} - {end_date}"


    def __str__(self):
        return f"{self.name} -> {self.start_date} - {self.end_date}"
    
    



