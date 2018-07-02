from django.db import models

from validators.phone_validator import validate_phone

class Subscriber(models.Model):
    phone_number = models.BigIntegerField(
        validators=[validate_phone],
        unique=True
    )

    def __str__(self):
        return self.phone_number


class CallStartRecord(models.Model):
    timestamp = models.DateTimeField(
        auto_now=False,
        auto_now_add=False
    )
    call_id = models.IntegerField(
    )
    source = models.BigIntegerField(
        validators=[validate_phone]
    )
    destination = models.BigIntegerField(
        validators=[validate_phone]
    )

    def __str__(self):
        return f'{self.source} - {self.destination}'

class CallEndRecord(models.Model):
    timestamp = models.DateTimeField(
        auto_now=False,
        auto_now_add=False
    )
    call_id = models.IntegerField(
    )

    def __str__(self):
        return str(self.call_id)
