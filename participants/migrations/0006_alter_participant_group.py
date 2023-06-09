# Generated by Django 4.1.3 on 2023-03-02 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0005_remove_participant_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant', to='participants.lottery'),
        ),
    ]
