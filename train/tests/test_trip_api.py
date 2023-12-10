from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train.models import (
    Trip,
    Crew,
    Route,
    Station,
    TrainType,
    Train
)

from train.serializers import (
    TripListOrRetrieveSerializer
)

TRIP_URL = reverse("train:trip-list")


def sample_crew(**params):
    defaults = {
        "first_name": "Sample first_name",
        "last_name": "Sample last_name",
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


def sample_station(**params):
    defaults = {
        "name": "st1",
        "latitude": 1.0,
        "longitude": 1.0
    }
    defaults.update(params)

    return Station.objects.create(**defaults)


def sample_type_train(**params):
    defaults = {
        "name": "test type"

    }
    defaults.update(params)

    return TrainType.objects.create(**defaults)


def sample_train(**params):
    defaults = {
        "name": "test train",
        "cargo_num": 2,
        "places_in_cargo": 3,
        "train_type": sample_type_train()
    }
    defaults.update(params)

    return Train.objects.create(**defaults)


def sample_route(**params):
    defaults = {
        "source": sample_station(name="st1"),
        "destination": sample_station(name="st2"),
        "distance": 3,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_trip(**params):
    defaults = {
        "route": sample_route(),
        "train": sample_train(),
        "departure_time": "2023-12-08T19:54:28+02:00",
        "arrival_time": "2023-12-10T19:54:28+02:00",
    }
    defaults.update(params)

    trip = Trip.objects.create(**defaults)
    trip.crews.set([sample_crew()])
    trip.tickets_available = 6
    return trip


def detail_trip_url(crew_id):
    return reverse("train:trip-detail", args=[crew_id])


class UnauthenticatedTripApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TRIP_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTripApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_filter_trip_by_arrival_time(self):
        trip1 = sample_trip(arrival_time="2023-12-09T19:54:28+02:00")
        trip2 = sample_trip(arrival_time="2023-12-10T19:54:28+02:00")
        trip3 = sample_trip(arrival_time="2023-12-10T19:54:28+02:00")

        res = self.client.get(TRIP_URL, {"arrival_time": "2023-12-10"})

        serializer1 = TripListOrRetrieveSerializer(trip1)
        serializer2 = TripListOrRetrieveSerializer(trip2)
        serializer3 = TripListOrRetrieveSerializer(trip3)
        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertIn(serializer3.data, res.data)

    def test_retrieve_crew_detail(self):
        crew = sample_crew(
            first_name="first_name",
            last_name="last_name"
        )
        trip = sample_trip()
        trip.crews.set([crew])
        url = detail_trip_url(trip.id)
        res = self.client.get(url)
        serializer = TripListOrRetrieveSerializer(trip)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_trip_forbidden(self):
        payload = {
            "route": sample_route(),
            "train": sample_train(),
            "departure_time": "2023-12-08T21:54:22+02:00",
            "arrival_time": "2023-12-09T21:54:22+02:00",
            "crews": sample_crew()
        }
        res = self.client.post(TRIP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTripApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_trip(self):
        crew = sample_crew()
        route = sample_route()
        payload = {
            "route": route.id,
            "train": sample_train().id,
            "departure_time": "2023-12-08T21:54:22+02:00",
            "arrival_time": "2023-12-09T21:54:22+02:00",
            "crews": [crew.id]
        }
        res = self.client.post(TRIP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload["departure_time"], res.data["departure_time"])
        self.assertEqual(payload["arrival_time"], res.data["arrival_time"])
