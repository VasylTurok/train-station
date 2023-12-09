from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from train.permissions import IsAdminOrIfAuthenticatedReadOnly

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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return CrewListOrRetrieveSerializer

        return self.serializer_class

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name")
        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "first_name",
                type=str,
                description="Filter by first_name. Example: ?full_name=qwe"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TrainTypeListOrRetrieveSerializer

        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="Filter by name. Example: ?name=qwe"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return RouteListOrRetrieveSerializers

        return self.serializer_class

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        queryset = self.queryset

        if source:
            queryset = queryset.filter(source__name__icontains=source)

        if destination:
            queryset = queryset.filter(destination__name__icontains=source)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=str,
                description="Filter by source. Example: ?source=Lviv"
            ),
            OpenApiParameter(
                "destination",
                type=str,
                description="Filter by destination. Example: ?destination=Kiev"
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="Filter by name. Example: ?name=qwe"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.select_related("train_type")
    serializer_class = TrainSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        train_type = self.request.query_params.get("train_type")
        queryset = self.queryset

        if train_type:
            queryset = queryset.filter(train_type__name__icontains=train_type)

        return queryset

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TrainListOrRetrieveSerializers

        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "train_type",
                type=str,
                description="Filter by train_type. Example: ?train_type=qwe"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related(
        "route",
        "train"
    ).prefetch_related(
        "crews"
    ).annotate(
        tickets_available=(
            F("train__cargo_num") * F("train__places_in_cargo")
            - Count("tickets")
        )
    )

    serializer_class = TripSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        departure_time = self.request.query_params.get("departure_time")
        arrival_time = self.request.query_params.get("arrival_time")

        queryset = self.queryset

        if departure_time:
            date = datetime.strptime(departure_time, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__date=date)

        if arrival_time:
            date = datetime.strptime(arrival_time, "%Y-%m-%d").date()
            queryset = queryset.filter(arrival_time__date=date)

        return queryset

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TripListOrRetrieveSerializer

        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "departure_time",
                type=str,
                description="Filter by departure_time. Example: ?arrival_time=2000-12-1"
            ),
            OpenApiParameter(
                "arrival_time",
                type=str,
                description="Filter by arrival_time. Example: ?arrival_time=2000-12-1"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("trip", "order")
    serializer_class = TicketSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TicketListSerializer

        return self.serializer_class

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the movies with filters"""
        trips = self.request.query_params.get("trips")

        queryset = self.queryset

        if trips:
            genres_ids = self._params_to_ints(trips)
            queryset = queryset.filter(trip__id__in=genres_ids)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "genres",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by genres id. Example: ?trips=1,3"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__trip__train", "tickets__trip__route"
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
