# Generated by Django 3.2.11 on 2022-01-20 08:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("fmea", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="FailureModeAffectedObject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "affected_department",
                    models.CharField(
                        choices=[
                            ("", "--- Select an option ----"),
                            ("Finances", "Finances"),
                            ("Marketing", "Marketing"),
                            ("Human Resources", "Human Resources"),
                            ("Research & Development", "Research & Development"),
                            ("Administration", "Administration"),
                            ("Service", "Service"),
                        ],
                        max_length=50,
                    ),
                ),
                ("affected_ooi_type", models.CharField(max_length=100)),
            ],
            options={"verbose_name_plural": "Failure Mode Affected Objects"},
        ),
        migrations.CreateModel(
            name="FailureModeTreeObject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tree_object", models.CharField(max_length=256)),
                (
                    "affected_department",
                    models.CharField(
                        choices=[
                            ("", "--- Select an option ----"),
                            ("Finances", "Finances"),
                            ("Marketing", "Marketing"),
                            ("Human Resources", "Human Resources"),
                            ("Research & Development", "Research & Development"),
                            ("Administration", "Administration"),
                            ("Service", "Service"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="failuremode",
            name="detectability_level",
            field=models.PositiveSmallIntegerField(
                choices=[
                    ("", "--- Select an option ----"),
                    (1, "Level 1: Always Detectable. Incident (almost) never occurs, almost unthinkable."),
                    (2, "Level 2: Usually Detectable. Incidents occur less than once a year (3-5)."),
                    (3, "Level 3: Detectable. Failure mode is detectable with effort."),
                    (4, "Level 4: Poorly Detectable. Detecting the failure mode is difficult."),
                    (5, "Level 5: Almost Undetectable. Failure mode detection is very difficult or nearly impossible."),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="failuremode", name="failure_mode", field=models.CharField(max_length=256, unique=True)
        ),
        migrations.AlterField(
            model_name="failuremode",
            name="frequency_level",
            field=models.PositiveSmallIntegerField(
                choices=[
                    ("", "--- Select an option ----"),
                    (1, "Level 1: Very Rare. Incident (almost) never occurs, almost unthinkable."),
                    (2, "Level 2: Rare. Incidents occur less than once a year (3-5)."),
                    (3, "Level 3: Occurs. Incidents occur several times a year."),
                    (4, "Level 4: Regularly. Incidents occur weekly."),
                    (5, "Level 5: Frequent. Incidents occur daily."),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="failuremode",
            name="severity_level",
            field=models.PositiveSmallIntegerField(
                choices=[
                    ("", "--- Select an option ----"),
                    (1, "Level 1: Not Severe"),
                    (2, "Level 2: Harmful"),
                    (3, "Level 3: Severe"),
                    (4, "Level 4: Very Harmful"),
                    (5, "Level 5: Catastrophic"),
                ]
            ),
        ),
        migrations.DeleteModel(name="FailureModeDepartment"),
        migrations.AddField(
            model_name="failuremodeaffectedobject",
            name="failure_mode",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="fmea.failuremode"),
        ),
    ]
