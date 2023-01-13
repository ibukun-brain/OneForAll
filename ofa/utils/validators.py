import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_age(value):
    now = timezone.now().date()
    age = (now - value).days // 365
    print(age)
    if age < 18:
        raise ValidationError(
            _('You are not up to 18 years old'),
            params={'value': value},
        )