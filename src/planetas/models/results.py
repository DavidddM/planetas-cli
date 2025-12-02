from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from .signs import ZodiacSign, Constellation


@dataclass(frozen=True)
class SignPosition:
    """
    Result of a single sign lookup query.

    Attributes:
        sign: The zodiac sign or constellation.
        longitude: Ecliptic longitude in degrees (0-360).
        longitude_in_sign: Degrees within the sign (0-30 for zodiac, variable for constellations).
    """

    sign: Union[ZodiacSign, Constellation]
    longitude: float
    longitude_in_sign: Optional[float] = None

    def format_longitude(self, precision: int = 2) -> str:
        """Format longitude as degrees/minutes/seconds string."""
        degrees = int(self.longitude)
        remainder = (self.longitude - degrees) * 60
        minutes = int(remainder)
        seconds = (remainder - minutes) * 60
        if precision == 0:
            return f"{degrees}°"
        if precision == 1:
            return f"{degrees}°{minutes:02d}'"
        return f"{degrees}°{minutes:02d}'{seconds:05.2f}\""


@dataclass(frozen=True)
class DateRange:
    """
    A continuous period when a planet occupied a specific sign.

    Attributes:
        start: Entry date/time into the sign.
        end: Exit date/time from the sign.
        sign: The sign occupied during this period.
    """

    start: datetime
    end: datetime
    sign: Union[ZodiacSign, Constellation]

    @property
    def duration_days(self) -> float:
        """Return duration in days."""
        delta = self.end - self.start
        return delta.total_seconds() / 86400

    def format_start(self, include_time: bool = False) -> str:
        """Format start date for display."""
        if include_time:
            return self.start.strftime("%Y-%m-%d %H:%M")
        return self.start.strftime("%Y-%m-%d")

    def format_end(self, include_time: bool = False) -> str:
        """Format end date for display."""
        if include_time:
            return self.end.strftime("%Y-%m-%d %H:%M")
        return self.end.strftime("%Y-%m-%d")

    @property
    def start_date(self) -> str:
        """Return start date as YYYY-MM-DD string."""
        return self.start.strftime("%Y-%m-%d")

    @property
    def start_time(self) -> str:
        """Return start time as HH:MM string."""
        return self.start.strftime("%H:%M")

    @property
    def end_date(self) -> str:
        """Return end date as YYYY-MM-DD string."""
        return self.end.strftime("%Y-%m-%d")

    @property
    def end_time(self) -> str:
        """Return end time as HH:MM string."""
        return self.end.strftime("%H:%M")


@dataclass(frozen=True)
class MultiSystemResult:
    """
    Result containing positions in multiple zodiac systems.

    Attributes:
        tropical: Position in tropical zodiac (None if not requested).
        sidereal: Position in sidereal zodiac (None if not requested).
        astronomical: Position in IAU constellations (None if not requested).
        date: The query date.
    """

    tropical: Optional[SignPosition]
    sidereal: Optional[SignPosition]
    astronomical: Optional[SignPosition]
    date: datetime
