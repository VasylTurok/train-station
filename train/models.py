from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class TrainType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.user.email)

    class Meta:
        ordering = ["-created_at"]


class Station(models.Model):
    name = models.CharField(max_length=63)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=63)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(
        TrainType,
        on_delete=models.CASCADE,
        related_name="trains"
    )

    @property
    def capacity(self) -> int:
        return self.cargo_num * self.places_in_cargo

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="destination_routes"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name}-{self.destination.name}"

    class Meta:
        unique_together = ("source", "destination")
        ordering = ["distance", ]


class Trip(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="trips"
    )
    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        related_name="trips"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crews = models.ManyToManyField(
        Crew,
        blank=True,
        related_name="trips"
    )

    def __str__(self):
        return f"{self.route} {self.departure_time}-{self.arrival_time}"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    @staticmethod
    def validate_ticket(cargo, seat, train, error_to_raise):
        for ticket_attr_value, ticket_attr_name, train_attr_name in [
            (cargo, "cargo", "cargo_num"),
            (seat, "seat", "places_in_cargo"),
        ]:
            count_attrs = getattr(train, train_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        "number must be in available "
                        f"(range: 1, {train_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.cargo,
            self.seat,
            self.trip.train,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{str(self.trip)} (row: {self.cargo}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("trip", "cargo", "seat")
        ordering = ["cargo", "seat"]
