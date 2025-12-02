from abc import ABC, abstractmethod
from datetime import datetime

from ..models import Planet, SignPosition


class BaseCalculator(ABC):
    """
    Abstract base class for zodiac position calculators.

    Subclasses implement specific zodiac systems (tropical, sidereal, astronomical).
    """

    @abstractmethod
    def get_sign(self, planet: Planet, dt: datetime) -> SignPosition | None:
        """
        Get the sign position for a planet at a specific datetime.

        Args:
            planet: The celestial body to query.
            dt: The datetime for the query (UTC).

        Returns:
            SignPosition with the sign and longitude, or None if position
            cannot be determined (e.g., planet in non-ecliptic constellation).
        """
        pass

    @abstractmethod
    def get_longitude(self, planet: Planet, dt: datetime) -> float:
        """
        Get the raw ecliptic longitude for a planet.

        Args:
            planet: The celestial body to query.
            dt: The datetime for the query (UTC).

        Returns:
            Ecliptic longitude in degrees (0-360).
        """
        pass

    @property
    @abstractmethod
    def system_name(self) -> str:
        """Return the name of this zodiac system."""
        pass
