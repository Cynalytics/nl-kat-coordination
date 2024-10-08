# Generated by Django 3.2.18 on 2023-05-11 12:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("tools", "0037_alter_organization_options")]

    operations = [
        migrations.AlterModelOptions(
            name="organization",
            options={
                "permissions": (
                    ("can_switch_organization", "Can switch organization"),
                    ("can_scan_organization", "Can scan organization"),
                    ("can_enable_disable_boefje", "Can enable or disable boefje"),
                    ("can_set_clearance_level", "Can set clearance level"),
                    ("can_delete_oois", "Can delete oois"),
                    ("can_mute_findings", "Can mute findings"),
                    ("can_view_katalogus_settings", "Can view KAT-alogus settings"),
                    ("can_set_katalogus_settings", "Can set KAT-alogus settings"),
                    ("can_recalculate_bits", "Can recalculate bits"),
                )
            },
        )
    ]
