from rest_framework import serializers
from django.db import transaction
from .models import (
    AstronomyShow,
    ShowTheme,
    ShowSession,
    PlanetariumDome,
    Ticket,
    Reservation,
)
from .validators import validate_seat_is_available


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class AstronomyShowSerializer(serializers.ModelSerializer):
    themes = ShowThemeSerializer(many=True, read_only=True)
    theme_ids = serializers.PrimaryKeyRelatedField(
        queryset=ShowTheme.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "name",
            "description",
            "duration_minutes",
            "poster",
            "themes",
            "theme_ids",
        )

    def _extract_theme_ids_from_initial(self):
        data = self.initial_data or {}
        if "themes" in data and isinstance(data["themes"], list):
            return ShowTheme.objects.filter(pk__in=data["themes"])
        return []

    def create(self, validated_data):
        theme_ids = validated_data.pop("theme_ids", None)
        if theme_ids is None:
            theme_ids = self._extract_theme_ids_from_initial()
        obj = AstronomyShow.objects.create(**validated_data)
        if theme_ids:
            obj.themes.set(theme_ids)
        return obj

    def update(self, instance, validated_data):
        theme_ids = validated_data.pop("theme_ids", None)
        if theme_ids is None:
            theme_ids = self._extract_theme_ids_from_initial()
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if theme_ids is not None:
            instance.themes.set(theme_ids)
        return instance


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row")


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show_detail = AstronomyShowSerializer(
        source="astronomy_show", read_only=True
    )
    cinema_hall_detail = PlanetariumDomeSerializer(source="cinema_hall", read_only=True)

    astronomy_show = serializers.PrimaryKeyRelatedField(
        queryset=AstronomyShow.objects.all(),
        write_only=True,
        required=True,
    )
    cinema_hall = serializers.PrimaryKeyRelatedField(
        queryset=PlanetariumDome.objects.all(),
        write_only=True,
        required=True,
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "astronomy_show",
            "cinema_hall",
            "astronomy_show_detail",
            "cinema_hall_detail",
            "start_time",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "reservation", "show_session", "row", "seat")

    def validate(self, attrs):
        show_session = attrs["show_session"]
        row = attrs["row"]
        seat = attrs["seat"]
        dome = show_session.cinema_hall
        if not (1 <= row <= dome.rows):
            raise serializers.ValidationError(f"Row must be in 1..{dome.rows}")
        if not (1 <= seat <= dome.seats_in_row):
            raise serializers.ValidationError(f"Seat must be in 1..{dome.seats_in_row}")
        validate_seat_is_available(show_session, row, seat)
        return attrs


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tickets = TicketSerializer(many=True, required=False)

    class Meta:
        model = Reservation
        fields = ("id", "user", "show_session", "created_at", "tickets")
        read_only_fields = ("created_at",)

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets", [])
        reservation = Reservation.objects.create(**validated_data)
        for t in tickets_data:
            Ticket.objects.create(reservation=reservation, **t)
        return reservation
