from rest_framework import serializers
from django.db import transaction
from .models import (
    AstronomyShow, ShowTheme, ShowSession,
    PlanetariumDome, Ticket, Reservation
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = "__all__"


class AstronomyShowSerializer(serializers.ModelSerializer):
    themes = ShowThemeSerializer(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ["id", "name", "description", "duration_minutes", "poster", "themes"]


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = "__all__"


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowSerializer(read_only=True)
    cinema_hall = PlanetariumDomeSerializer(read_only=True)

    class Meta:
        model = ShowSession
        fields = ["id", "astronomy_show", "cinema_hall", "start_time"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "reservation", "show_session", "row", "seat"]


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ["id", "user", "show_session", "created_at", "tickets"]
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        with transaction.atomic():
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
        return reservation
