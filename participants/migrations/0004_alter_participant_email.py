# Generated by Django 4.1.3 on 2023-03-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0003_participant_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]
