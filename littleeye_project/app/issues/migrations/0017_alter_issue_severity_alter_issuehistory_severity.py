# Generated by Django 4.1.3 on 2023-07-14 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0016_alter_issue_severity_alter_issue_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='severity',
            field=models.IntegerField(choices=[(1, 'normal'), (2, 'dringend'), (3, 'sofort')], default=1),
        ),
        migrations.AlterField(
            model_name='issuehistory',
            name='severity',
            field=models.IntegerField(choices=[(1, 'normal'), (2, 'dringend'), (3, 'sofort')]),
        ),
    ]