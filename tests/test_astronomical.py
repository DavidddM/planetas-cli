"""
Astronomical (IAU constellation) position verification tests.

Uses IAU constellation boundaries defined in 1930.
Notable: Ophiuchus is the 13th ecliptic constellation.
"""

import json
import pytest

from planetas.cli import main


class TestAstronomicalBasics:
    """Basic IAU constellation functionality."""

    def test_astronomical_mode_works(self, cli_runner):
        """Astronomical mode should return a constellation."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-06-15", "-s", "astronomical"
        ])
        assert result.exit_code == 0
        assert "astronomical" in result.output.lower()

    def test_ophiuchus_in_constellation_list(self, cli_runner):
        """Ophiuchus should be listed in available constellations."""
        result = cli_runner.invoke(main, ["list-signs"])
        assert result.exit_code == 0
        assert "ophiuchus" in result.output.lower()


class TestSunInOphiuchus:
    """
    Verify the Sun enters Ophiuchus around Nov 30 and exits around Dec 17.

    This is the key differentiator between astronomical and zodiac systems.
    In tropical/sidereal, the Sun is in Sagittarius during this period.
    """

    def test_sun_in_scorpius_late_november(self, cli_runner):
        """Sun should be in Scorpius (IAU) around Nov 24-29."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-11-25", "-s", "astronomical"
        ])
        assert result.exit_code == 0
        assert "scorpius" in result.output.lower()

    @pytest.mark.parametrize("date", ["2025-12-05", "2025-12-10", "2025-12-15"])
    def test_sun_in_ophiuchus(self, cli_runner, date):
        """Sun should be in Ophiuchus from ~Nov 30 to ~Dec 17."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", date, "-s", "astronomical"
        ])
        assert result.exit_code == 0
        assert "ophiuchus" in result.output.lower()

    def test_sun_exits_ophiuchus_to_sagittarius(self, cli_runner):
        """Sun exits Ophiuchus and enters Sagittarius around Dec 17-18."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-12-20", "-s", "astronomical"
        ])
        assert result.exit_code == 0
        assert "sagittarius" in result.output.lower()

    def test_sun_tropical_sagittarius_during_ophiuchus(self, cli_runner):
        """While astronomically in Ophiuchus, tropically the Sun is in Sagittarius."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-12-05", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "sagittarius" in result.output.lower()


class TestScorpiusVsScorpio:
    """
    Compare IAU Scorpius (~6 days) vs tropical Scorpio (~30 days).

    IAU Scorpius: approximately Nov 23-29
    Tropical Scorpio: Oct 23 - Nov 21
    """

    def test_sun_tropical_scorpio_early_november(self, cli_runner):
        """Sun is in tropical Scorpio in early November."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-11-10", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "scorpio" in result.output.lower()

    def test_sun_not_scorpius_early_november(self, cli_runner):
        """Sun is NOT in IAU Scorpius in early November (still in Libra)."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-11-10", "-s", "astronomical"
        ])
        assert result.exit_code == 0
        assert "scorpius" not in result.output.lower()

    def test_sun_tropical_sagittarius_when_astronomical_scorpius(self, cli_runner):
        """Around Nov 25, Sun is in IAU Scorpius but tropical Sagittarius."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-11-25", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "sagittarius" in result.output.lower()


class TestAstronomicalRanges:
    """Test date range searches with astronomical constellations."""

    def test_sun_ophiuchus_range(self, cli_runner, sun_ophiuchus_dates):
        """Search for Sun in Ophiuchus during 2025 (~Nov 30 - Dec 17)."""
        result = cli_runner.invoke(main, [
            "ranges", "-p", "sun", "-g", sun_ophiuchus_dates["constellation"],
            "-s", "2025-01-01", "-e", "2025-12-31",
            "--system", "astronomical", "-f", "json"
        ])
        assert result.exit_code == 0

        data = json.loads(result.output)

        assert len(data) >= 1, "Expected at least 1 Ophiuchus period for Sun"

        start = data[0]["start_date"]
        assert "11" in start or "12" in start, "Ophiuchus period should be in Nov/Dec"

    def test_sun_scorpius_range_is_short(self, cli_runner):
        """Sun in Scorpius (IAU) should be ~6-7 days, not 30."""
        result = cli_runner.invoke(main, [
            "ranges", "-p", "sun", "-g", "scorpius",
            "-s", "2025-01-01", "-e", "2025-12-31",
            "--system", "astronomical", "-f", "json"
        ])
        assert result.exit_code == 0

        data = json.loads(result.output)

        if len(data) > 0:
            duration = data[0].get("duration_days", 0)
            assert duration < 15, f"Scorpius duration should be ~6-7 days, got {duration}"


class TestCompareAllSystems:
    """Compare positions across all three systems."""

    def test_december_sun_three_systems(self, cli_runner, known_positions):
        """
        Sun on Dec 10, 2025:
        - Tropical: Sagittarius
        - Sidereal (Lahiri): Scorpio
        - Astronomical: Ophiuchus

        All three different!
        """
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-12-10", "-s", "all"
        ])
        assert result.exit_code == 0
        output = result.output.lower()

        assert "sagittarius" in output
        assert "ophiuchus" in output
