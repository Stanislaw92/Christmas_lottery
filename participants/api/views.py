from inspect import GEN_RUNNING
import json
import random
from django.http import JsonResponse
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


import os
from twilio.rest import Client


import time
import smtplib
from email.message import EmailMessage

from participants.api.permissions import IsAuthorOrReadyOnly, IsAuthorOrReadyOnlyForParticipant
from participants.api.serializers import ParticipantSerializer, LotterySerializer, LotteryResultSerializer
from participants.models import Participant, Lottery, LotteryResult


def getUser(request):
    user = request.user
    return user


class LotteryViewSet(viewsets.ModelViewSet):
    queryset = Lottery.objects.all().order_by('-created_at')
    serializer_class = LotterySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadyOnly]
    lookup_field = "uuid"

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        return super().perform_create(serializer)

    def get_queryset(self):
        user = self.request.user
        return Lottery.objects.filter(creator=user).order_by('-created_at')





class ParticipantCreateAPIView(generics.CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        kwarg_uuid = self.kwargs.get('uuid')
        lottery = get_object_or_404(Lottery, uuid=kwarg_uuid)
        serializer.save(group=lottery)


class ParticipantRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadyOnlyForParticipant]
    lookup_field = 'uuid'


class ParticipantListAPIView(generics.ListAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_uuid = self.kwargs.get('uuid')
        return Participant.objects.filter(group__uuid=kwarg_uuid).order_by("-group__created_at")


class LotteryResultCreateAPIView(generics.CreateAPIView):
    queryset = LotteryResult.objects.all()
    serializer_class = LotteryResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        kwarg_uuid = self.kwargs.get('uuid')
        lottery = get_object_or_404(Lottery, uuid=kwarg_uuid)
        serializer.save(group=lottery)


class LotteryResultRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LotteryResult.objects.all()
    serializer_class = LotteryResultSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadyOnlyForParticipant]
    lookup_field = 'uuid'

# class LotteryResultListAPIView(generics.RetrieveAPIView):
#     serializer_class = LotteryResultSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field='uuid'

#     def get_queryset(self):
#         queryset = LotteryResult.objects.all()
#         kwarg_uuid = self.kwargs.get('uuid')


class LotteryResultAPIView(APIView):

    def get_object(self, uuid):
        lottery_result = get_object_or_404(LotteryResult, group__uuid=uuid)
        return lottery_result

    def get(self, request, uuid):
        lottery_result = self.get_object(uuid)
        serializer = LotteryResultSerializer(lottery_result)
        return Response(serializer.data)

        # return queryset.filter(group__uuid=kwarg_uuid).order_by("-group__created_at")
        # x = get_object_or_404(LotteryResult, group__uuid=kwarg_uuid)
        # print('x', x)
        # return get_object_or_404(LotteryResult, group__uuid=kwarg_uuid)
        # return LotteryResult.objects.filter(group__uuid=kwarg_uuid).order_by("-group__created_at")


def LotteryResultFunc(request):
    context = {}
    if request.method == 'POST':
        participants = []
        for i in request.POST.getlist('participants'):
            unStringiFied = json.loads(i)
            participants.append(unStringiFied)
        emailMsg = request.POST.get('emailMsg')
        textMsg = request.POST.get('textMsg')
        lotteryUuid = request.POST.get('uuid')

        whoArr = []

        for i in participants:
            whoArr.append(i)

        random.shuffle(whoArr)
        Allright = False
        counter = 0

        try:
            while Allright == False:
                whomArr = []
                resultArr = []
                for i in participants:
                    whomArr.append(i)

                for i in whoArr:
                    whomResult = random.choice(whomArr)
                    if i['relation'] != whomResult['relation'] or i['relation'] == 1 and i['name'] != whomResult['name']:
                        Allright = True
                    else:
                        while_counter = 0
                        while i['relation'] == whomResult['relation']:
                            while_counter += 1
                            whomResult = random.choice(whomArr)
                            Allright = True
                            if while_counter >= 10:
                                Allright = False
                                break
                    if Allright == True:
                        resultArr.append(
                            (i['name'], whomResult['name'], whomResult['email']))
                        whomArr.remove(whomResult)
                        counter += 1
                    else:
                        break
            successVar = True
            print(resultArr)
        except Exception as e:
            print('e:', e)
            successVar = False

        if successVar == True:
            lotteryObj = get_object_or_404(Lottery, uuid=lotteryUuid)
            resultObj = LotteryResult(group=lotteryObj, result=resultArr)
            resultObj.save()

            SendingEmails(resultArr)

            context = {
                'successVar': successVar, 'resultDict': resultArr
            }
        else:
            context = {
                'successVar': successVar
            }
    return JsonResponse(context)


def SendingEmails(WhoList):

    # SMS sending function, need payed account to sending sms's

    # account_sid = "AC57316ff217424736cfbc7f93bbf475f6"
    # auth_token = "8d97576382f67dd26de1ce82896d22df"
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    # body="Cześć Patsi, jak tam Twój norweski ;-)",
    # from_="+16128873099",
    # to="+48519677139"
    # )

    count = 0
    for i in WhoList:
        count += 1
        forWho = '{}'.format(WhoList[count-1][1])
        whoMaking = '{}'.format(i[0])
        # mailTo = '{}'.format(i[2])
        mailTo = 'vrnyfci551@vigoneo.com'  # Test E-mail
        user = 'stachuu2@gmail.com'
        password = 'bqydmxjxemxzyofg'

        print(count)
        print('{} robi prezent {}'.format(whoMaking, forWho))

        msg = EmailMessage()
        msg['Subject'] = 'Christmas Lottery!'
        msg['From'] = user
        msg['To'] = mailTo
        msg.set_content('''
            <!doctype html>
            <html lang="en">
            <head>
                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">


                <!-- Bootstrap CSS -->
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">

                <title>Lottery</title>
            </head>
            <body style="
                background-image: linear-gradient(326deg, #d3d3d3 0%, #ff6b6b 74%);
            ">
                <div style="
                    padding:5px 0px;
                    display: flex;
                    justify-content: center;
                    align-items: flex-start;
                    height: 92vh;
                    ">
                    <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    height: 500px;
                    width: 80%;
                    ">
                        <img src="https://parade.com/.image/t_share/MTkzMDUzMTIxMDY3MzYxNTAx/best-christmas-gifts.jpg" style="height: 300px;">
                        <div style="
                        text-align:center;
                        margin-top: 10px;
                        ">
                            <h3>Congratulation!
                            </h3>
                            <p style="
                                font-size: 20px;
                            ">You are making a present for <b>{}</b> ! </p>
                        </div>
                    </div>
                </div>



                <!-- Bootstrap Bundle with Popper -->
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>
                <!-- Jquery -->
                <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
            </body>
            </html>
            '''.format(forWho), subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
