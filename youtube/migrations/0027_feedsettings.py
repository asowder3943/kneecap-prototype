# Generated by Django 4.1.4 on 2023-01-06 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("youtube", "0026_rename_inititalized_channel_initialized"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "feed_order",
                    models.CharField(default="chronological", max_length=255),
                ),
            ],
            options={
                "verbose_name": "Feed Settings",
            },
        ),
    ]
