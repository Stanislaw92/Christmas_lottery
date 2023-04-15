from django.contrib import admin
from participants.models import Participant, Lottery, LotteryResult

admin.site.register(Participant)
admin.site.register(Lottery)
admin.site.register(LotteryResult)
