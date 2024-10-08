# Generated by Django 3.2.15 on 2022-10-27 12:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("tools", "0024_auto_20221005_1251")]

    operations = [
        migrations.AlterModelOptions(
            name="organization",
            options={
                "permissions": (
                    ("can_switch_organization", "Can switch organization"),
                    ("can_scan_organization", "Can scan organization"),
                    ("can_enable_disable_boefje", "Can enable or disable boefje"),
                    ("can_set_clearance_level", "Can set clearance level"),
                )
            },
        ),
        migrations.AlterField(
            model_name="organizationmember",
            name="acknowledged_clearance_level",
            field=models.IntegerField(
                default=-1,
                validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(4)],
            ),
        ),
        migrations.AlterField(
            model_name="organizationmember",
            name="trusted_clearance_level",
            field=models.IntegerField(
                default=-1,
                validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(4)],
            ),
        ),
    ]
