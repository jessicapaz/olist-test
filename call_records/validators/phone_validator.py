from django.core.exceptions import ValidationError


def validate_phone(phone):
    phone_length = len(str(phone))

    if phone_length > 11 or phone_length < 10:
        raise ValidationError(
            f'{phone} is not a valid phone number, the size must be 10 or 11.',
            params={'phone': phone},
        )
