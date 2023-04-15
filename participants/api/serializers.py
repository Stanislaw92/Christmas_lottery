from rest_framework import serializers

from participants.models import Participant, Lottery, LotteryResult


class ParticipantSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    groups_uuid = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        exclude = ["id"]

    def get_groups_uuid(self, instance):
        return instance.group.uuid


class LotterySerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    num_of_participants = serializers.SerializerMethodField()
    have_result = serializers.SerializerMethodField()

    class Meta:
        model = Lottery
        exclude = ['updated_at']

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_num_of_participants(self, instance):
        return instance.participant.count()

    def get_have_result(self, instance):
        return instance.get_result()


class LotteryResultSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()

    class Meta:
        model = LotteryResult
        exclude = ["id"]

