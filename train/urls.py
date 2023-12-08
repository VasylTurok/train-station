from django.urls import path, include
from rest_framework import routers

from train.views import (
    CrewViewSet,
    TrainTypeViewSet,
    RouteViewSet
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("routes", RouteViewSet)


urlpatterns = router.urls

app_name = "train"
