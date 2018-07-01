from django.core.exceptions import ValidationError

def validate_phone(phone):
    if len(phone) < 10:
        raise ValidationError(
            f'{phone} is not a valid phone number, the size must be greater than 10.',
            params={'phone': phone},
        )