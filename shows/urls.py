from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import (
    AstronomyShowViewSet,
    ShowThemeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
    TicketViewSet,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


router = DefaultRouter()
router.register("shows", AstronomyShowViewSet)
router.register("themes", ShowThemeViewSet)
router.register("sessions", ShowSessionViewSet)
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("tickets", TicketViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("shows.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("", RedirectView.as_view(url="/api/schema/swagger-ui/", permanent=False)),
]
