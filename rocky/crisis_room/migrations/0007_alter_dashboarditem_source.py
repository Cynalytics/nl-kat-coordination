# Generated by Django 5.1.10 on 2025-06-18 07:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("crisis_room", "0006_rename_dashboarddata_dashboarditem")]

    operations = [
        migrations.AlterField(
            model_name="dashboarditem", name="source", field=models.CharField(blank=True, max_length=126)
        )
    ]
