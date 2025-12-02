"""
CLI smoke tests - verify commands don't crash and produce expected output structure.
"""

import csv
import io
import json
import pytest
from click.testing import CliRunner
from planetas.cli import main


class TestCLIBasics:
    """Basic CLI functionality tests."""
    
    def test_help_command(self, cli_runner):
        result = cli_runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Zodiac Position Finder" in result.output or "planetas" in result.output.lower()
    
    def test_sign_help(self, cli_runner):
        result = cli_runner.invoke(main, ["sign", "--help"])
        assert result.exit_code == 0
        assert "--planet" in result.output
        assert "--date" in result.output
    
    def test_ranges_help(self, cli_runner):
        result = cli_runner.invoke(main, ["ranges", "--help"])
        assert result.exit_code == 0
        assert "--planet" in result.output
        assert "--sign" in result.output
    
    def test_list_planets(self, cli_runner):
        result = cli_runner.invoke(main, ["list-planets"])
        assert result.exit_code == 0
        assert "jupiter" in result.output.lower()
        assert "saturn" in result.output.lower()
        assert "moon" in result.output.lower()
    
    def test_list_signs(self, cli_runner):
        result = cli_runner.invoke(main, ["list-signs"])
        assert result.exit_code == 0
        assert "aries" in result.output.lower()
        assert "pisces" in result.output.lower()
    
    def test_list_ayanamsas(self, cli_runner):
        result = cli_runner.invoke(main, ["list-ayanamsas"])
        assert result.exit_code == 0
        assert "lahiri" in result.output.lower()


class TestSignCommand:
    """Tests for the 'sign' command."""
    
    def test_sign_basic(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "2025-06-15"
        ])
        assert result.exit_code == 0
        assert "jupiter" in result.output.lower()
    
    def test_sign_all_systems(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "mars", "-d", "2025-01-01", "-s", "all"
        ])
        assert result.exit_code == 0
        assert "tropical" in result.output.lower()
        assert "sidereal" in result.output.lower()
        assert "astronomical" in result.output.lower()
    
    def test_sign_tropical_only(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "venus", "-d", "2025-03-15", "-s", "tropical"
        ])
        assert result.exit_code == 0
        assert "tropical" in result.output.lower()
    
    def test_sign_sidereal_with_ayanamsa(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "moon", "-d", "2025-01-01", 
            "-s", "sidereal", "-a", "lahiri"
        ])
        assert result.exit_code == 0
        assert "sidereal" in result.output.lower()
    
    def test_sign_invalid_planet(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "notaplanet", "-d", "2025-01-01"
        ])
        assert result.exit_code != 0
        assert "error" in result.output.lower() or "unknown" in result.output.lower()
    
    def test_sign_invalid_date(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "jupiter", "-d", "not-a-date"
        ])
        assert result.exit_code != 0


class TestRangesCommand:
    """Tests for the 'ranges' command."""
    
    def test_ranges_basic(self, cli_runner):
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "aquarius",
            "-s", "2020-01-01", "-e", "2022-12-31"
        ])
        assert result.exit_code == 0
        assert "2020" in result.output or "2021" in result.output
    
    def test_ranges_json_output(self, cli_runner):
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "taurus",
            "-s", "2023-01-01", "-e", "2024-12-31",
            "--system", "tropical", "-f", "json"
        ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert isinstance(data, list)
        if len(data) > 0:
            assert "start_date" in data[0]
            assert "end_date" in data[0]
    
    def test_ranges_csv_output(self, cli_runner):
        result = cli_runner.invoke(main, [
            "ranges", "-p", "saturn", "-g", "aquarius",
            "-s", "2020-01-01", "-e", "2023-12-31",
            "--system", "tropical", "-f", "csv"
        ])
        assert result.exit_code == 0
        reader = csv.reader(io.StringIO(result.output))
        headers = next(reader)
        assert "start_date" in headers
        assert "end_date" in headers
    
    def test_ranges_invalid_date_order(self, cli_runner):
        result = cli_runner.invoke(main, [
            "ranges", "-p", "jupiter", "-g", "aries",
            "-s", "2025-01-01", "-e", "2020-01-01"
        ])
        assert result.exit_code != 0


class TestAllPlanets:
    """Verify all planets work with basic queries."""
    
    @pytest.mark.parametrize("planet", [
        "sun", "moon", "mercury", "venus", "mars",
        "jupiter", "saturn", "uranus", "neptune", "pluto",
    ])
    def test_planet_sign_lookup(self, cli_runner, planet):
        result = cli_runner.invoke(main, [
            "sign", "-p", planet, "-d", "2025-01-01"
        ])
        assert result.exit_code == 0


class TestPrecisionOption:
    """Test precision flag."""
    
    def test_day_precision_default(self, cli_runner):
        result = cli_runner.invoke(main, [
            "sign", "-p", "moon", "-d", "2025-01-01"
        ])
        assert result.exit_code == 0
    
    def test_minute_precision(self, cli_runner):
        result = cli_runner.invoke(main, [
            "--precision", "minute",
            "sign", "-p", "moon", "-d", "2025-01-01 12:00"
        ])
        assert result.exit_code == 0
