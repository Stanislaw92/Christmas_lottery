from django.urls import include, path
from rest_framework.routers import DefaultRouter

from participants.api import views as qv

router = DefaultRouter()
router.register(r"lotteries", qv.LotteryViewSet)


urlpatterns = [
    path("", include(router.urls)),

    path("lotteries/<uuid:uuid>/participants/",qv.ParticipantListAPIView.as_view(), name='answer-list'),

    path("lotteries/<uuid:uuid>/participant/",qv.ParticipantCreateAPIView.as_view(), name='answer-create'),

    path("participants/<uuid:uuid>/",qv.ParticipantRUDAPIView.as_view(), name='answer-detail'),
]