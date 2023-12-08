from django.urls import path, include
from rest_framework import routers

from train.views import (
    CrewViewSet,
    TrainTypeViewSet,
    RouteViewSet,
    StationViewSet
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("routes", RouteViewSet)
router.register("stations", StationViewSet)

urlpatterns = router.urls

app_name = "train"
