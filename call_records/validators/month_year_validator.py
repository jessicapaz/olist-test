from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_month(month):
    if month > 12 or month < 1:
        raise ValidationError(
            f'{month} is not a valid month, the period must be between 1 and 12.'
        )

def validate_year(year):
    current_year = timezone.now().year

    if year > current_year:
        raise ValidationError(
            f'{year} is not a valid year, the year must be less or equal the current year.'
        )