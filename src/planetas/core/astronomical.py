from datetime import datetime

import swisseph as swe
from skyfield.api import load_constellation_map, position_of_radec

from .base import BaseCalculator
from ..config import Config
from ..models import Planet, Constellation, SignPosition


class AstronomicalCalculator(BaseCalculator):
    """
    Calculator for IAU constellation positions.

    Uses Swiss Ephemeris for planetary positions and Skyfield
    for constellation boundary lookup.

    Returns one of 13 ecliptic constellations including Ophiuchus.
    """

    _constellation_map = None

    def __init__(self) -> None:
        """Initialize the calculator and load required data."""
        ephe_path = Config.get_ephemeris_path()
        swe.set_ephe_path(str(ephe_path))
        self._init_skyfield()

    def _init_skyfield(self) -> None:
        """Initialize Skyfield constellation map."""
        if AstronomicalCalculator._constellation_map is None:
            AstronomicalCalculator._constellation_map = load_constellation_map()

    @property
    def system_name(self) -> str:
        return "astronomical (IAU)"

    def get_longitude(self, planet: Planet, dt: datetime) -> float:
        """
        Get tropical ecliptic longitude for a planet.

        Note: IAU constellations use equatorial coordinates (RA/Dec),
        but we still provide ecliptic longitude for reference.

        Args:
            planet: The celestial body to query.
            dt: The datetime for the query (UTC).

        Returns:
            Tropical ecliptic longitude in degrees (0-360).
        """
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0 + dt.second / 3600.0)
        result, _ = swe.calc_ut(jd, int(planet))
        return result[0] % 360

    def _get_equatorial_position(self, planet: Planet, dt: datetime) -> tuple[float, float]:
        """
        Get equatorial coordinates (RA, Dec) for a planet.

        Args:
            planet: The celestial body to query.
            dt: The datetime for the query (UTC).

        Returns:
            Tuple of (right_ascension_hours, declination_degrees).
        """
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0 + dt.second / 3600.0)
        result, _ = swe.calc_ut(jd, int(planet), swe.FLG_EQUATORIAL)
        ra_degrees = result[0]
        dec_degrees = result[1]
        ra_hours = ra_degrees / 15.0
        return ra_hours, dec_degrees

    def get_sign(self, planet: Planet, dt: datetime) -> SignPosition | None:
        """
        Get the IAU constellation for a planet.

        Args:
            planet: The celestial body to query.
            dt: The datetime for the query (UTC).

        Returns:
            SignPosition with IAU constellation, or None if the planet is
            in a non-ecliptic constellation.
        """
        ra_hours, dec_degrees = self._get_equatorial_position(planet, dt)

        position = position_of_radec(ra_hours, dec_degrees)
        constellation_abbrev = AstronomicalCalculator._constellation_map(position)

        constellation = Constellation.from_abbreviation(constellation_abbrev)
        if constellation is None:
            return None

        longitude = self.get_longitude(planet, dt)

        return SignPosition(
            sign=constellation,
            longitude=longitude,
            longitude_in_sign=None,
        )
