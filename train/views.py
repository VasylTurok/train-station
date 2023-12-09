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
    TrainListOrRetrieveSerializers,
    TripListOrRetrieveSerializer
)


class Pagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.prefetch_related("trips")
    serializer_class = CrewSerializer
    pagination_class = Pagination

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


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.select_related("train_type")
    serializer_class = TrainSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TrainListOrRetrieveSerializers

        return self.serializer_class


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related(
        "route",
        "train"
    ).prefetch_related("crews")
    serializer_class = TripSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TripListOrRetrieveSerializer

        return self.serializer_class


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TicketListSerializer

        return self.serializer_class


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie", "tickets__movie_session__cinema_hall"
    )
    serializer_class = OrderSerializer
    pagination_class = Pagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
