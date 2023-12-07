from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from train.models import (
    Ticket,
    Train,
    Trip,
    TrainType,
    Route,
    Station,
    Order,
    Crew
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"
