from django.urls import path, include
from rest_framework import routers

from train.views import (
    CrewViewSet,
    TrainTypeViewSet,

)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("train-types", TrainTypeViewSet)


urlpatterns = router.urls

app_name = "train"
