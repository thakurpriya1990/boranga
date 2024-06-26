# Generated by Django 3.2.25 on 2024-05-23 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boranga", "0253_auto_20240521_1607"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="conservationstatus",
            name="cs_end_date",
        ),
        migrations.RemoveField(
            model_name="conservationstatus",
            name="cs_start_date",
        ),
        migrations.RemoveField(
            model_name="conservationstatus",
            name="delisting_date",
        ),
        migrations.AlterField(
            model_name="conservationstatus",
            name="approval_level",
            field=models.CharField(
                choices=[("intermediate", "Intermediate"), ("minister", "Ministerial")],
                max_length=20,
                null=True,
            ),
        ),
    ]
