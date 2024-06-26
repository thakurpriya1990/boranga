# Generated by Django 3.2.25 on 2024-04-12 01:48

import boranga.components.conservation_status.models
import boranga.components.meetings.models
import boranga.components.occurrence.models
import boranga.components.species_and_communities.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boranga", "0217_occurrence_report_amendment_referral_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="occurrence",
            name="effective_from",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="occurrence",
            name="effective_to",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="occurrence",
            name="review_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="occurrence",
            name="review_due_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="occurrence",
            name="review_status",
            field=models.CharField(
                choices=[
                    ("not_reviewed", "Not Reviewed"),
                    ("awaiting_amendments", "Awaiting Amendments"),
                    ("amended", "Amended"),
                    ("accepted", "Accepted"),
                ],
                default="not_reviewed",
                max_length=30,
                verbose_name="Review Status",
            ),
        ),
        migrations.AddField(
            model_name="occurrence",
            name="reviewed_by",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="occurrencereport",
            name="review_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="occurrencereport",
            name="review_due_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="occurrencereport",
            name="reviewed_by",
            field=models.IntegerField(null=True),
        ),
    ]
