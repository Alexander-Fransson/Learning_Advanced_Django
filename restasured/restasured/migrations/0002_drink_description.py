# Generated by Django 4.1.7 on 2023-03-05 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restasured', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drink',
            name='description',
            field=models.CharField(default='something', max_length=500),
            preserve_default=False,
        ),
    ]
