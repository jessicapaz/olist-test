from django.db import models

from validators.phone_validator import validate_phone
from validators.month_year_validator import validate_month, validate_year

class Subscriber(models.Model):
    first_name = models.CharField(
        max_length=30
    )
    last_name = models.CharField(
        max_length=30
    )
    phone_number = models.BigIntegerField(
        validators=[validate_phone],
        unique=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


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

class BillRecord(models.Model):
    subscriber = models.ForeignKey(
        'Subscriber',
        on_delete=models.PROTECT
    )
    call_start_record = models.ForeignKey(
        "CallStartRecord",
        on_delete=models.SET_NULL,
        null=True
    )
    call_duration = models.TimeField()
    reference_month = models.IntegerField(
        validators=[validate_month]
    )
    reference_year = models.IntegerField(
        validators=[validate_year]
    )
    call_price = models.DecimalField(
        max_digits=6,
        decimal_places=3
    )