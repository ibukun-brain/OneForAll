from django.db import models


class Gender(models.TextChoices):
    Male = ("male", "Male")
    Female = ("female", "Female")
    Other = ("other", "Other")

class Status(models.TextChoices):
    Single = ("Single", "Single")
    Married = ("Married", "Married")
