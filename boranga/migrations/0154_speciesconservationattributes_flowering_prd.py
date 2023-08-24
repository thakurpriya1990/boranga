# Generated by Django 3.2.20 on 2023-08-03 03:42

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('boranga', '0153_auto_20230802_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='speciesconservationattributes',
            name='flowering_prd',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('january', 'January'), ('february', 'February'), ('march', 'March')], max_length=250, null=True),
        ),
    ]