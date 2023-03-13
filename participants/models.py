import uuid as uuid_lib

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from core.models import TimeStampedModel

from users.models import CustomUser

class Lottery(TimeStampedModel):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=50, default='')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lottery_group')

    class Meta:
        verbose_name_plural = "Lotteries"

    def __str__(self):
        return self.name

class Participant(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    group = models.ForeignKey(Lottery, on_delete=models.CASCADE, related_name='participant')
    relation = models.SmallIntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    

    def __str__(self):
        return self.name + " " + self.surname