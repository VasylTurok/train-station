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
    CrewListOrRetrieveSerializer
)

CREW_URL = reverse("train:crew-list")


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


def detail_crew_url(crew_id):
    return reverse("train:crew-detail", args=[crew_id])


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_crews(self):
        sample_crew()
        sample_crew()

        res = self.client.get(CREW_URL)

        crews = Crew.objects.order_by("id")
        serializer = CrewListOrRetrieveSerializer(crews, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_crews_by_first_name(self):
        crew1 = sample_crew(first_name="some name")
        crew2 = sample_crew(first_name="Another name")
        crew3 = sample_crew(first_name="No match")

        res = self.client.get(CREW_URL, {"first_name": "name"})

        serializer1 = CrewListOrRetrieveSerializer(crew1)
        serializer2 = CrewListOrRetrieveSerializer(crew2)
        serializer3 = CrewListOrRetrieveSerializer(crew3)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_retrieve_crew_detail(self):
        crew = sample_crew()
        route = Route.objects.create(
            source=sample_station(),
            destination=sample_station(name="st2"),
            distance=1
        )
        train = Train.objects.create(
            name="tr1",
            cargo_num=12,
            places_in_cargo=10,
            train_type=TrainType.objects.create(
                name="type1"
            )
        )
        trip1 = Trip.objects.create(
            departure_time="2023-12-08T21:54:22+02:00",
            arrival_time="2023-12-09T21:54:22+02:00",
            route=route,
            train=train
        )
        crew.trips.add(trip1)

        url = detail_crew_url(crew.id)
        res = self.client.get(url)

        serializer = CrewListOrRetrieveSerializer(crew)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_crew_forbidden(self):
        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }
        res = self.client.post(CREW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_crew(self):
        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }
        res = self.client.post(CREW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        crew = Crew.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(crew, key))

    def test_create_crew_with_trips(self):
        route = Route.objects.create(
            source=sample_station(),
            destination=sample_station(name="st2"),
            distance=1
        )
        train = Train.objects.create(
            name="tr1",
            cargo_num=12,
            places_in_cargo=10,
            train_type=TrainType.objects.create(
                name="type1"
            )
        )
        trip1 = Trip.objects.create(
            departure_time="2023-12-08T21:54:22+02:00",
            arrival_time="2023-12-09T21:54:22+02:00",
            route=route,
            train=train
        )
        trip2 = Trip.objects.create(
            departure_time="2023-11-08T21:54:22+02:00",
            arrival_time="2023-11-09T21:54:22+02:00",
            route=route,
            train=train
        )
        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
            "trips": [trip1.id, trip2.id]
        }
        res = self.client.post(CREW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        crew = Crew.objects.get(id=res.data["id"])
        trips = crew.trips.all()
        self.assertEqual(trips.count(), 2)
        self.assertIn(trip1, trips)
        self.assertIn(trip2, trips)
