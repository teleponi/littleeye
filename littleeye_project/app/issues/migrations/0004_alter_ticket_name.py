# Generated by Django 4.1.3 on 2023-08-13 20:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0003_remove_mediatype_icon_remove_tag_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='name',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
