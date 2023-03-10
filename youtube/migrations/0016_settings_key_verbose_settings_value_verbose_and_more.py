# Generated by Django 4.1.4 on 2022-12-31 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("youtube", "0015_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="key_verbose",
            field=models.CharField(
                default="Feed Order",
                max_length=255,
                verbose_name="Setting Key Verbose Name",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="settings",
            name="value_verbose",
            field=models.CharField(
                default="Chronological Order",
                max_length=255,
                verbose_name="Setting Value Verbose Name",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="settings",
            name="key",
            field=models.CharField(
                max_length=255, unique=True, verbose_name="Setting Key"
            ),
        ),
        migrations.AlterField(
            model_name="settings",
            name="value",
            field=models.CharField(max_length=255, verbose_name="Setting Value"),
        ),
    ]
