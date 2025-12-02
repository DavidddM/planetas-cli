"""
Tropical zodiac position verification tests.

Uses verified ingress data to confirm planetary positions are calculated correctly.
"""

import json
import pytest

from planetas.cli import main


class TestJupiterTropical:
    """Verify Jupiter tropical positions against known ingress dates."""

    @pytest.mark.parametrize("date,expected_sign", [
        ("2020-12-20", "aquarius"),   # Entered 2020-12-19 13:07 UTC
        ("2021-05-14", "pisces"),     # Entered 2021-05-13
        ("2021-08-15", "aquarius"),   # Retrograde back 2021-07-28
        ("2022-05-11", "aries"),      # Entered 2022-05-10
        ("2023-05-17", "taurus"),     # Entered 2023-05-16
        ("2024-05-26", "gemini"),     # Entered 2024-05-25
        ("2025-06-10", "cancer"),     # Entered 2025-06-09
    ])
    def test_jupiter_ingress(self, cli_runner, date, expected_sign):
        """Verify Jupiter is in expected sign after each ingress date."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", date, "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert expected_sign in result.output.lower()

    def test_jupiter_in_capricorn_before_aquarius_ingress(self, cli_runner):
        """Jupiter should be in Capricorn on 2020-12-18 (day before Aquarius ingress)."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2020-12-18", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "capricorn" in result.output.lower()


class TestSaturnTropical:
    """Verify Saturn tropical positions against known ingress dates."""

    @pytest.mark.parametrize("date,expected_sign", [
        ("2020-03-23", "aquarius"),   # First entered 2020-03-22
        ("2020-07-15", "capricorn"),  # Retrograde back 2020-07-01
        ("2020-12-18", "aquarius"),   # Re-entered 2020-12-17
        ("2023-03-08", "pisces"),     # Entered 2023-03-07
    ])
    def test_saturn_ingress(self, cli_runner, date, expected_sign):
        """Verify Saturn is in expected sign after each ingress date."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "saturn", "-d", date, "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert expected_sign in result.output.lower()

    def test_saturn_in_pisces_2024(self, cli_runner):
        """Saturn should be in Pisces throughout 2024."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "saturn", "-d", "2024-06-15", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "pisces" in result.output.lower()


class TestMarsTropical:
    """Verify Mars tropical positions including retrograde cycle."""

    @pytest.mark.parametrize("date,expected_sign", [
        ("2024-09-05", "cancer"),     # Entered 2024-09-04
        ("2024-11-15", "leo"),        # Entered 2024-11-04
        ("2025-01-15", "cancer"),     # Retrograde back 2025-01-06
        ("2025-04-20", "leo"),        # Re-entered 2025-04-18
        ("2025-06-20", "virgo"),      # Entered 2025-06-17
    ])
    def test_mars_ingress(self, cli_runner, date, expected_sign):
        """Verify Mars is in expected sign after each ingress date."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "mars", "-d", date, "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert expected_sign in result.output.lower()


class TestMoonTropical:
    """Verify Moon tropical positions - fast moving body verification."""

    @pytest.mark.parametrize("datetime_str,expected_sign", [
        ("2025-01-01 12:00", "aquarius"),  # Entered 10:49 UTC
        ("2025-01-03 18:00", "pisces"),    # Entered 15:21 UTC
        ("2025-01-05 22:00", "aries"),     # Entered 19:01 UTC
        ("2025-01-08 06:00", "taurus"),    # Entered 2025-01-07 22:11 UTC
    ])
    def test_moon_ingress(self, cli_runner, datetime_str, expected_sign):
        """Verify Moon is in expected sign after each ingress time."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "moon", "-d", datetime_str, "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert expected_sign in result.output.lower()


class TestRangesVerification:
    """Verify date range search against known ingress data."""

    def test_jupiter_aquarius_ranges_2020_2022(self, cli_runner):
        """
        Jupiter was in Aquarius during two periods:
        1. 2020-12-19 to 2021-05-13 (direct)
        2. 2021-07-28 to 2021-12-29 (retrograde return)
        """
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "aquarius",
            "-s", "2020-01-01", "-e", "2022-12-31",
            "--system", "tropical", "-f", "json"
        ])
        assert result.exit_code == 0

        data = json.loads(result.output)

        assert len(data) >= 2, "Expected at least 2 Aquarius periods for Jupiter"

        starts = [d["start_date"] for d in data]
        assert any("2020-12" in s for s in starts), "Missing Dec 2020 ingress"
        assert any("2021-07" in s or "2021-08" in s for s in starts), "Missing Jul 2021 retrograde ingress"

    def test_saturn_aquarius_ranges(self, cli_runner):
        """
        Saturn was in Aquarius during:
        1. 2020-03-22 to 2020-07-01 (first entry)
        2. 2020-12-17 to 2023-03-07 (main transit)
        """
        result = cli_runner.invoke(main, [
            "ranges", "-p", "saturn", "-g", "aquarius",
            "-s", "2020-01-01", "-e", "2024-12-31",
            "--system", "tropical", "-f", "json"
        ])
        assert result.exit_code == 0

        data = json.loads(result.output)

        assert len(data) >= 2, "Expected at least 2 Aquarius periods for Saturn"
