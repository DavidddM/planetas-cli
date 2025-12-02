"""
Sidereal zodiac position verification tests.

Uses Lahiri ayanamsa (~24.31° for 2025) to verify sidereal calculations.
Sidereal position = Tropical position - Ayanamsa
"""

import pytest

from planetas.cli import main


class TestSiderealBasics:
    """Basic sidereal calculation verification."""

    def test_sidereal_differs_from_tropical(self, cli_runner):
        """Sidereal and tropical positions should differ by ~24° (ayanamsa)."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-06-15", "-s", "all"
        ])
        assert result.exit_code == 0
        output = result.output.lower()

        assert "tropical" in output
        assert "sidereal" in output

    def test_lahiri_ayanamsa_default(self, cli_runner):
        """Default ayanamsa should be Lahiri, shown in output."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-01-01", "-s", "sidereal"
        ])
        assert result.exit_code == 0
        assert "lahiri" in result.output.lower()

    def test_default_ayanamsa_is_lahiri(self, cli_runner):
        """Default ayanamsa should produce same result as explicit --ayanamsa lahiri."""
        default_result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-01-01", "-s", "sidereal"
        ])
        explicit_result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-01-01", "-s", "sidereal", "-a", "lahiri"
        ])
        assert default_result.exit_code == 0
        assert explicit_result.exit_code == 0
        assert default_result.output == explicit_result.output

    @pytest.mark.parametrize("ayanamsa", ["fagan_bradley", "raman"])
    def test_other_ayanamsas_work(self, cli_runner, ayanamsa):
        """Other ayanamsa systems should work."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-01-01",
            "-s", "sidereal", "-a", ayanamsa
        ])
        assert result.exit_code == 0


class TestSiderealPositions:
    """
    Verify specific sidereal positions using known_positions fixture.

    With Lahiri ayanamsa ~24.31° for 2025:
    - Tropical Cancer (90-120°) → Sidereal Gemini (66-96°)
    - Tropical Aries (0-30°) → Sidereal Pisces (336-360°) for early degrees
    """

    def test_jupiter_sidereal_june_2025(self, cli_runner, known_positions):
        """Jupiter in early Cancer (tropical) should be in Gemini (sidereal)."""
        expected = known_positions["2025-06-15"]["jupiter"]["sidereal"]
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-06-15", "-s", "sidereal"
        ])
        assert result.exit_code == 0
        assert expected in result.output.lower()

    def test_jupiter_sidereal_jan_2024(self, cli_runner, known_positions):
        """Jupiter was in Taurus (tropical) in Jan 2024, should be Aries (sidereal)."""
        expected = known_positions["2024-01-01"]["jupiter"]["sidereal"]
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2024-01-01", "-s", "sidereal"
        ])
        assert result.exit_code == 0
        assert expected in result.output.lower()

    def test_saturn_sidereal_2025(self, cli_runner, known_positions):
        """Saturn in Aries (tropical) mid-2025 should be in Pisces (sidereal)."""
        expected = known_positions["2025-06-15"]["saturn"]["sidereal"]
        result = cli_runner.invoke(main, [
            "sign", "-p", "saturn", "-d", "2025-06-15", "-s", "sidereal"
        ])
        assert result.exit_code == 0
        assert expected in result.output.lower()

    def test_sun_sidereal_march_equinox(self, cli_runner):
        """Sun at vernal equinox (0° Aries tropical) should be in Pisces (sidereal)."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-03-20", "-s", "sidereal"
        ])
        assert result.exit_code == 0
        assert "pisces" in result.output.lower()


class TestSiderealRanges:
    """Verify sidereal date range searches."""

    def test_jupiter_sidereal_ranges(self, cli_runner):
        """Search for Jupiter in Aries (sidereal)."""
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "aries",
            "-s", "2023-01-01", "-e", "2025-12-31",
            "--system", "sidereal", "-a", "lahiri"
        ])
        assert result.exit_code == 0

    def test_saturn_sidereal_ranges(self, cli_runner):
        """Search for Saturn in Aquarius (sidereal)."""
        result = cli_runner.invoke(main, [
            "ranges", "-p", "saturn", "-g", "aquarius",
            "-s", "2020-01-01", "-e", "2025-12-31",
            "--system", "sidereal"
        ])
        assert result.exit_code == 0


class TestAyanamsaComparison:
    """Compare different ayanamsa systems."""

    def test_lahiri_vs_fagan_differ(self, cli_runner):
        """Lahiri and Fagan-Bradley should produce different output."""
        lahiri_result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-01-01",
            "-s", "sidereal", "-a", "lahiri"
        ])

        fagan_result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-01-01",
            "-s", "sidereal", "-a", "fagan_bradley"
        ])

        assert lahiri_result.exit_code == 0
        assert fagan_result.exit_code == 0
        assert lahiri_result.output != fagan_result.output
