from rest_framework import routers

from train.views import (
    CrewViewSet,
    TrainTypeViewSet,
    RouteViewSet,
    StationViewSet,
    TrainViewSet,
    TripViewSet,
    TicketViewSet
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("routes", RouteViewSet)
router.register("stations", StationViewSet)
router.register("trains", TrainViewSet)
router.register("trip", TripViewSet)
router.register("tickets", TicketViewSet)


urlpatterns = router.urls

app_name = "train"
