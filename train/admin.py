from django.contrib import admin

from .models import (
    Trip,
    Train,
    TrainType,
    Ticket,
    Station,
    Route,
    Crew,
    Order
)


admin.site.register(Trip)
admin.site.register(Train)
admin.site.register(Ticket)
admin.site.register(TrainType)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Crew)
admin.site.register(Order)
