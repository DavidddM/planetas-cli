from datetime import datetime

import swisseph as swe

from .base import BaseCalculator
from ..config import Config
from ..models import Planet, ZodiacSign, SignPosition


class TropicalCalculator(BaseCalculator):
    """
    Calculator for tropical zodiac positions.

    Uses Swiss Ephemeris with default (tropical) settings.
    Zodiac is anchored to the vernal equinox.
    """

    def __init__(self) -> None:
        """Initialize the calculator and set ephemeris path."""
        ephe_path = Config.get_ephemeris_path()
        swe.set_ephe_path(str(ephe_path))

    @property
    def system_name(self) -> str:
        return "tropical"

    def get_longitude(self, planet: Planet, dt: datetime) -> float:
        """
        Get tropical ecliptic longitude for a planet.

        Args:
            planet: The celestial body to query.
            dt: The datetime for the query (UTC).

        Returns:
            Tropical ecliptic longitude in degrees (0-360).
        """
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0 + dt.second / 3600.0)
        result, _ = swe.calc_ut(jd, int(planet))
        longitude = result[0]
        return longitude % 360

    def get_sign(self, planet: Planet, dt: datetime) -> SignPosition | None:
        """
        Get the tropical zodiac sign for a planet.

        Args:
            planet: The celestial body to query.
            dt: The datetime for the query (UTC).

        Returns:
            SignPosition with tropical sign and longitude.
        """
        longitude = self.get_longitude(planet, dt)
        sign = ZodiacSign.from_longitude(longitude)
        longitude_in_sign = longitude % 30
        return SignPosition(
            sign=sign,
            longitude=longitude,
            longitude_in_sign=longitude_in_sign,
        )
