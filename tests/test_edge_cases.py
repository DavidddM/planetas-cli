"""
Edge case and boundary condition tests.

Tests for sign boundaries, date edge cases, and unusual inputs.
"""

import csv
import io
import json

from planetas.cli import main


class TestSignBoundaries:
    """Test behavior at exact sign boundaries (0°, 30°, 60°, etc.)."""
    
    def test_vernal_equinox_is_aries(self, cli_runner):
        """
        Vernal equinox (Sun at 0° ecliptic longitude) should be Aries.
        
        March 20, 2025 is approximately the vernal equinox.
        """
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-03-20 12:00", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "aries" in result.output.lower()
    
    def test_summer_solstice_is_cancer(self, cli_runner):
        """
        Summer solstice (Sun at 90°) should be Cancer.
        
        June 21, 2025 is approximately the summer solstice.
        """
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-06-21 12:00", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "cancer" in result.output.lower()
    
    def test_autumn_equinox_is_libra(self, cli_runner):
        """
        Autumn equinox (Sun at 180°) should be Libra.
        
        September 22, 2025 is approximately the autumn equinox.
        """
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-09-22 19:00", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "libra" in result.output.lower()
    
    def test_winter_solstice_is_capricorn(self, cli_runner):
        """
        Winter solstice (Sun at 270°) should be Capricorn.
        
        December 21, 2025 is approximately the winter solstice.
        """
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2025-12-21 16:00", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "capricorn" in result.output.lower()


class TestDateEdgeCases:
    """Test unusual date inputs."""
    
    def test_year_1_ad(self, cli_runner):
        """Test calculation for year 1 AD (if ephemeris supports it)."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "0001-06-15", "-s", "tropical"
        ])
        if result.exit_code == 0:
            assert any(sign in result.output.lower() for sign in [
                "aries", "taurus", "gemini", "cancer", "leo", "virgo",
                "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
            ])
    
    def test_year_2100(self, cli_runner):
        """Test calculation for year 2100."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "saturn", "-d", "2100-01-01", "-s", "tropical"
        ])
        assert result.exit_code == 0
    
    def test_leap_year_feb_29(self, cli_runner):
        """Test February 29 on a leap year."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "sun", "-d", "2024-02-29", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "pisces" in result.output.lower()
    
    def test_date_with_time(self, cli_runner):
        """Test date with time component."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "moon", "-d", "2025-01-15 14:30", "-s", "tropical"
        ])
        assert result.exit_code == 0
    
    def test_iso_format_date(self, cli_runner):
        """Test ISO 8601 format date."""
        result = cli_runner.invoke(main, [
            "sign", "-p", "venus", "-d", "2025-06-15T12:00:00", "-s", "tropical"
        ])
        assert result.exit_code == 0


class TestInvalidInputs:
    """Test error handling for invalid inputs."""
    
    def test_invalid_planet_name(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "krypton", "-d", "2025-01-01"
        ])
        assert result.exit_code != 0
    
    def test_invalid_sign_name(self, cli_runner):
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "notasign",
            "-s", "2020-01-01", "-e", "2025-12-31"
        ])
        assert result.exit_code != 0
    
    def test_invalid_ayanamsa(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-01-01",
            "-s", "sidereal", "-a", "notanayanamsa"
        ])
        assert result.exit_code != 0
    
    def test_invalid_system(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-01-01",
            "-s", "notasystem"
        ])
        assert result.exit_code != 0
    
    def test_missing_required_planet(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-d", "2025-01-01"
        ])
        assert result.exit_code != 0
    
    def test_missing_required_date(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter"
        ])
        assert result.exit_code != 0


class TestOutputFormats:
    """Test different output format options."""
    
    def test_table_format_default(self, cli_runner):
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "taurus",
            "-s", "2023-01-01", "-e", "2024-12-31"
        ])
        assert result.exit_code == 0
        assert "Start" in result.output or "start" in result.output.lower()
    
    def test_json_format_valid(self, cli_runner):
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "taurus",
            "-s", "2023-01-01", "-e", "2024-12-31",
            "--system", "tropical", "-f", "json"
        ])
        assert result.exit_code == 0
        
        data = json.loads(result.output)
        assert isinstance(data, list)
    
    def test_csv_format_valid(self, cli_runner):
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "taurus",
            "-s", "2023-01-01", "-e", "2024-12-31",
            "--system", "tropical", "-f", "csv"
        ])
        assert result.exit_code == 0

        reader = csv.reader(io.StringIO(result.output))
        rows = list(reader)
        assert len(rows) >= 1


class TestLongRangeSearch:
    """Test searches over long date ranges."""
    
    def test_jupiter_12_year_cycle(self, cli_runner):
        """
        Jupiter has ~12 year orbital period.
        Should find ~1 occurrence of Jupiter in any sign per 12 years.
        """
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "taurus",
            "-s", "2000-01-01", "-e", "2025-12-31",
            "-f", "json"
        ])
        assert result.exit_code == 0
        
        data = json.loads(result.output)
        
        assert len(data) >= 2, "Expected ~2 Taurus periods in 25 years"
    
    def test_saturn_30_year_cycle(self, cli_runner):
        """
        Saturn has ~30 year orbital period.
        Should find ~1 occurrence of Saturn in any sign per 30 years.
        """
        result = cli_runner.invoke(main, [
            "ranges", "-p", "saturn", "-g", "aquarius",
            "-s", "1990-01-01", "-e", "2025-12-31",
            "-f", "json"
        ])
        assert result.exit_code == 0
        
        data = json.loads(result.output)
        
        assert len(data) >= 1, "Expected at least 1 Aquarius period in 35 years"
