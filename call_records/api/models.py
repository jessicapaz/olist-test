from django.db import models

from validators.phone_validator import validate_phone

class Subscriber(models.Model):
    phone_number = models.CharField(
        max_length=11,
        validators=[validate_phone],
        unique=True
    )

    def __str__(self):
        return self.phone_number
