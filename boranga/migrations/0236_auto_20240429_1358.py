# Generated by Django 3.2.25 on 2024-04-29 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boranga", "0235_add_new_occurrence_name_field_to_approval_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="occurrencereportapprovaldetails",
            name="new_occurrence_name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddIndex(
            model_name="occurrence",
            index=models.Index(
                fields=["community"], name="boranga_occ_communi_fe6716_idx"
            ),
        ),
    ]
