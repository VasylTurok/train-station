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
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "trips"
        )


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "cargo_num",
            "places_in_cargo",
            "train_type",
            "capacity"
        )


class TrainListOrRetrieveSerializers(TrainSerializer):
    train_type = serializers.CharField(
        source="train_type.name",
        read_only=True
    )


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance"
        )


class RouteListOrRetrieveSerializers(RouteSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(
        source="destination.name",
        read_only=True
    )


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            "id",
            "route",
            "train",
            "departure_time",
            "arrival_time",
            "crews"
        )


class CrewForTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("full_name",)


class TripListOrRetrieveSerializer(TripSerializer):
    train = serializers.CharField(source="train.name", read_only=True)
    crews = CrewForTripSerializer(many=True, read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta(TripSerializer.Meta):
        fields = (
            "id",
            "route",
            "train",
            "departure_time",
            "arrival_time",
            "crews",
            "tickets_available"
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["cargo"],
            attrs["seat"],
            attrs["trip"].train,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "trip")


class TicketListSerializer(TicketSerializer):
    trip = TripListOrRetrieveSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)


class CrewListOrRetrieveSerializer(CrewSerializer):
    trips = TripSerializer(many=True, read_only=True)


class TrainTypeListOrRetrieveSerializer(TrainTypeSerializer):
    class Meta(TrainTypeSerializer.Meta):
        fields = (
            "id",
            "name",
            "trains"
        )
