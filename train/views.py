from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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

from train.serializers import (
    CrewSerializer,

)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.prefetch_related("trips")
    serializer_class = CrewSerializer
