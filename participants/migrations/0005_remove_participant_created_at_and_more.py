# Generated by Django 4.1.3 on 2023-03-02 18:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0004_alter_participant_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='lottery',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
