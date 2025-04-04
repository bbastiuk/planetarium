from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AstronomyShowViewSet,
    ShowThemeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
    TicketViewSet,
)

router = DefaultRouter()
router.register("shows", AstronomyShowViewSet)
router.register("themes", ShowThemeViewSet)
router.register("sessions", ShowSessionViewSet)
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("tickets", TicketViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
