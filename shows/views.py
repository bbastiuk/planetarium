from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch

from .models import (
    AstronomyShow, ShowTheme, ShowSession,
    PlanetariumDome, Ticket, Reservation
)
from .serializers import (
    AstronomyShowSerializer, ShowThemeSerializer, ShowSessionSerializer,
    ReservationSerializer, TicketSerializer
)
from .permissions import IsOwnerOrReadOnly
from .validators import validate_seat_is_available


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("themes").all()
    serializer_class = AstronomyShowSerializer
    permission_classes = [permissions.AllowAny]


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = [permissions.AllowAny]


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related("cinema_hall", "astronomy_show").all()
    serializer_class = ShowSessionSerializer
    permission_classes = [permissions.AllowAny]


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).prefetch_related("tickets")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="my")
    def my_reservations(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("reservation", "show_session").all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        show_session = serializer.validated_data["show_session"]
        row = serializer.validated_data["row"]
        seat = serializer.validated_data["seat"]
        validate_seat_is_available(show_session, row, seat)
        serializer.save()
