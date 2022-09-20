from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_started_date(value):
    today = timezone.now().date()
    if value > today:
        raise ValidationError(f"The started date of an investment only can be today or a date in the past.")
