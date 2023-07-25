# Generated by Django 4.1.3 on 2023-07-23 15:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0017_alter_issue_severity_alter_issuehistory_severity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ['-severity', 'status']},
        ),
        migrations.RemoveConstraint(
            model_name='issue',
            name='unique_author',
        ),
        migrations.AlterField(
            model_name='issue',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.IntegerField(choices=[(0, 'neu eingestellt'), (1, 'in Bearbeitung'), (2, 'erledigt'), (3, 'geschlossen')], default=0),
        ),
        migrations.AddConstraint(
            model_name='issue',
            constraint=models.UniqueConstraint(fields=('author', 'name', 'created_at'), name='unique_author'),
        ),
    ]
