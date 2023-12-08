from rest_framework import routers

from train.views import (
    CrewViewSet,
    TrainTypeViewSet,
    RouteViewSet,
    StationViewSet,
    TrainViewSet
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("routes", RouteViewSet)
router.register("stations", StationViewSet)
router.register("trains", TrainViewSet)

urlpatterns = router.urls

app_name = "train"
