from datetime import datetime

import swisseph as swe

from .base import BaseCalculator
from ..config import Config
from ..models import Planet, ZodiacSign, Ayanamsa, SignPosition


class SiderealCalculator(BaseCalculator):
    """
    Calculator for sidereal zodiac positions.

    Uses Swiss Ephemeris with sidereal mode enabled.
    Zodiac is anchored to fixed stars, offset by the selected ayanamsa.
    """

    def __init__(self, ayanamsa: Ayanamsa = Ayanamsa.LAHIRI) -> None:
        """
        Initialize the calculator with specified ayanamsa.

        Args:
            ayanamsa: The ayanamsa system to use. Defaults to Lahiri.
        """
        self._ayanamsa = ayanamsa
        ephe_path = Config.get_ephemeris_path()
        swe.set_ephe_path(str(ephe_path))

    @property
    def ayanamsa(self) -> Ayanamsa:
        """Return the configured ayanamsa."""
        return self._ayanamsa

    @property
    def system_name(self) -> str:
        return f"sidereal ({self._ayanamsa.display_name})"

    def _datetime_to_jd(self, dt: datetime) -> float:
        """Convert datetime to Julian Day using Swiss Ephemeris."""
        return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0 + dt.second / 3600.0)

    def get_ayanamsa_value(self, dt: datetime) -> float:
        """
        Get the ayanamsa offset value for a specific date.

        Args:
            dt: The datetime for the query (UTC).

        Returns:
            Ayanamsa offset in degrees.
        """
        jd = self._datetime_to_jd(dt)
        return swe.get_ayanamsa_ut(jd)

    def get_longitude(self, planet: Planet, dt: datetime) -> float:
        """
        Get sidereal ecliptic longitude for a planet.

        Args:
            planet: The celestial body to query.
            dt: The datetime for the query (UTC).

        Returns:
            Sidereal ecliptic longitude in degrees (0-360).
        """
        jd = self._datetime_to_jd(dt)
        swe.set_sid_mode(int(self._ayanamsa))
        result, _ = swe.calc_ut(jd, int(planet), swe.FLG_SIDEREAL)
        longitude = result[0]
        return longitude % 360

    def get_sign(self, planet: Planet, dt: datetime) -> SignPosition | None:
        """
        Get the sidereal zodiac sign for a planet.

        Args:
            planet: The celestial body to query.
            dt: The datetime for the query (UTC).

        Returns:
            SignPosition with sidereal sign and longitude.
        """
        longitude = self.get_longitude(planet, dt)
        sign = ZodiacSign.from_longitude(longitude)
        longitude_in_sign = longitude % 30
        return SignPosition(
            sign=sign,
            longitude=longitude,
            longitude_in_sign=longitude_in_sign,
        )
