# Generated by Django 4.2.2 on 2023-07-01 21:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0008_remove_tag_description_alter_issue_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
