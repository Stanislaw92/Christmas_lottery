# Generated by Django 4.1.3 on 2023-03-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_alter_lottery_options_lottery_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='email',
            field=models.EmailField(default='', max_length=100),
        ),
    ]
