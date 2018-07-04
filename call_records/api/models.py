from django.db import models

from validators.phone_validator import validate_phone


class Subscriber(models.Model):
    phone_number = models.BigIntegerField(
        validators=[validate_phone],
        unique=True
    )

    def __str__(self):
        return str(self.phone_number)


class CallStartRecord(models.Model):
    timestamp = models.DateTimeField()
    call_id = models.IntegerField(
        unique=True
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
    timestamp = models.DateTimeField()
    call_id = models.IntegerField(
        unique=True
    )

    def __str__(self):
        return str(self.call_id)


class Price(models.Model):
    TARRIF_CHOICES = (
        ('standard', 'standard'),
        ('reduced', 'reduced')
    )
    tarrif_type = models.CharField(
        max_length=8,
        choices=TARRIF_CHOICES
    )
    standing_charge = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    call_charge = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )