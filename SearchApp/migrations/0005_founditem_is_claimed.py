# Generated by Django 5.1.7 on 2025-07-04 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SearchApp", "0004_alter_lostitem_description_founditem"),
    ]

    operations = [
        migrations.AddField(
            model_name="founditem",
            name="is_claimed",
            field=models.BooleanField(default=False),
        ),
    ]
