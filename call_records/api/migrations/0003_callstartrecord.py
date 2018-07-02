# Generated by Django 2.0.6 on 2018-07-01 19:10

from django.db import migrations, models
import validators.phone_validator


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180701_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallStartRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('call_id', models.IntegerField(unique=True)),
                ('source', models.BigIntegerField(validators=[validators.phone_validator.validate_phone])),
                ('destination', models.BigIntegerField(validators=[validators.phone_validator.validate_phone])),
            ],
        ),
    ]