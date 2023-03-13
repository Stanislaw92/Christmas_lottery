from inspect import GEN_RUNNING
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from participants.api.permissions import IsAuthorOrReadyOnly, IsAuthorOrReadyOnlyForParticipant
from participants.api.serializers import ParticipantSerializer, LotterySerializer
from participants.models import Participant, Lottery


class LotteryViewSet(viewsets.ModelViewSet):
    queryset = Lottery.objects.all().order_by('-created_at')
    serializer_class = LotterySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadyOnly]
    lookup_field = "uuid"

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        return super().perform_create(serializer)


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
