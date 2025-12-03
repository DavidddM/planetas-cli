from datetime import datetime, timedelta
from typing import Generator

from ..core.base import BaseCalculator
from ..models import Planet, ZodiacSign, Constellation, DateRange


class RangeFinder:
    """
    Finds all date ranges when a planet occupied a specific sign.

    Uses adaptive stepping with binary search refinement at sign boundaries.
    Handles retrograde motion correctly by detecting re-entries.
    """

    def __init__(self, calculator: BaseCalculator) -> None:
        """
        Initialize the range finder with a calculator.

        Args:
            calculator: The zodiac calculator to use for position queries.
        """
        self._calculator = calculator

    def find_ranges(
        self,
        planet: Planet,
        target_sign: ZodiacSign | Constellation,
        start_date: datetime,
        end_date: datetime,
    ) -> Generator[DateRange, None, None]:
        """
        Find all date ranges when a planet was in a specific sign.

        Args:
            planet: The celestial body to track.
            target_sign: The sign to search for.
            start_date: Start of search range (UTC).
            end_date: End of search range (UTC).

        Yields:
            DateRange objects for each continuous period in the sign.
        """
        step_days = planet.search_step_days
        step = timedelta(days=step_days)

        current = start_date
        in_sign = False
        entry_date: datetime | None = None

        while current <= end_date:
            position = self._calculator.get_sign(planet, current)
            current_sign = position.sign if position else None
            current_in_sign = self._signs_match(current_sign, target_sign)

            if current_in_sign and not in_sign:
                if current == start_date:
                    entry_date = start_date
                else:
                    entry_date = self._find_boundary(
                        planet, target_sign, current - step, current,
                        find_entry=True,
                    )
                in_sign = True

            elif not current_in_sign and in_sign:
                exit_date = self._find_boundary(
                    planet, target_sign, current - step, current,
                    find_entry=False,
                )
                if entry_date is not None:
                    yield DateRange(
                        start=entry_date,
                        end=exit_date,
                        sign=target_sign,
                    )
                in_sign = False
                entry_date = None

            current += step

        if in_sign and entry_date is not None:
            final_position = self._calculator.get_sign(planet, end_date)
            final_sign = final_position.sign if final_position else None
            if self._signs_match(final_sign, target_sign):
                yield DateRange(
                    start=entry_date,
                    end=end_date,
                    sign=target_sign,
                )
            else:
                search_start = min(current - step, end_date)
                exit_date = self._find_boundary(
                    planet, target_sign, search_start, end_date,
                    find_entry=False,
                )
                yield DateRange(
                    start=entry_date,
                    end=exit_date,
                    sign=target_sign,
                )

    def _signs_match(
        self,
        sign1: ZodiacSign | Constellation | None,
        sign2: ZodiacSign | Constellation,
    ) -> bool:
        """Check if two signs are equal. Returns False if sign1 is None."""
        if sign1 is None:
            return False
        return sign1 == sign2

    def _find_boundary(
        self,
        planet: Planet,
        target_sign: ZodiacSign | Constellation,
        before: datetime,
        after: datetime,
        find_entry: bool,
    ) -> datetime:
        """
        Binary search to find exact boundary (entry or exit) for a sign.

        Args:
            planet: The celestial body.
            target_sign: The sign.
            before: Datetime known to be before boundary.
            after: Datetime known to be after boundary.
            find_entry: True to find entry point, False to find exit point.

        Returns:
            Datetime of boundary (to minute precision).
        """
        min_delta = timedelta(minutes=1)

        while (after - before) > min_delta:
            mid = before + (after - before) / 2
            position = self._calculator.get_sign(planet, mid)
            mid_sign = position.sign if position else None
            mid_in_sign = self._signs_match(mid_sign, target_sign)

            if find_entry == mid_in_sign:
                after = mid
            else:
                before = mid

        result = after if find_entry else before
        return result.replace(second=0, microsecond=0)
