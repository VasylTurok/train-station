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
    TrainTypeSerializer,
    TripSerializer,
    TicketSerializer,
    TicketListSerializer,
    TrainSerializer,
    RouteSerializer,
    OrderSerializer,
    OrderListSerializer,
    StationSerializer,
    CrewListOrRetrieveSerializer,
    TrainTypeListOrRetrieveSerializer,
    RouteListOrRetrieveSerializers,

)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.prefetch_related("trips")
    serializer_class = CrewSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return CrewListOrRetrieveSerializer

        return self.serializer_class


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TrainTypeListOrRetrieveSerializer

        return self.serializer_class


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return RouteListOrRetrieveSerializers

        return self.serializer_class


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
