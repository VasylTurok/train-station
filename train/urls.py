from django.urls import path, include
from rest_framework import routers

from train.views import (
    CrewViewSet,
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)

urlpatterns = router.urls

app_name = "train"
