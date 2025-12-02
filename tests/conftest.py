import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    """Provide a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def jupiter_ingresses_tropical():
    """
    Verified Jupiter tropical ingress data 2020-2025.
    
    Format: (date_str, sign, direction)
    Times are approximate to the day for day-precision testing.
    """
    return [
        ("2020-12-19", "aquarius", "direct"),
        ("2021-05-13", "pisces", "direct"),
        ("2021-07-28", "aquarius", "retrograde"),
        ("2021-12-29", "pisces", "direct"),
        ("2022-05-10", "aries", "direct"),
        ("2022-10-28", "pisces", "retrograde"),
        ("2022-12-20", "aries", "direct"),
        ("2023-05-16", "taurus", "direct"),
        ("2024-05-25", "gemini", "direct"),
        ("2025-06-09", "cancer", "direct"),
    ]


@pytest.fixture
def saturn_ingresses_tropical():
    """
    Verified Saturn tropical ingress data 2020-2025.
    
    Format: (date_str, sign, direction)
    """
    return [
        ("2020-03-22", "aquarius", "direct"),
        ("2020-07-01", "capricorn", "retrograde"),
        ("2020-12-17", "aquarius", "direct"),
        ("2023-03-07", "pisces", "direct"),
        ("2025-05-25", "aries", "direct"),
    ]


@pytest.fixture
def mars_ingresses_2025():
    """
    Verified Mars tropical ingress data 2024-2025.
    
    Includes retrograde cycle for edge case testing.
    """
    return [
        ("2024-09-04", "cancer", "direct"),
        ("2024-11-04", "leo", "direct"),
        ("2025-01-06", "cancer", "retrograde"),
        ("2025-04-18", "leo", "direct"),
        ("2025-06-17", "virgo", "direct"),
    ]


@pytest.fixture
def moon_ingresses_jan_2025():
    """
    Verified Moon tropical ingress data for January 2025.
    
    Format: (date_str, time_utc, sign)
    """
    return [
        ("2025-01-01", "10:49", "aquarius"),
        ("2025-01-03", "15:21", "pisces"),
        ("2025-01-05", "19:01", "aries"),
        ("2025-01-07", "22:11", "taurus"),
        ("2025-01-10", "01:06", "gemini"),
        ("2025-01-12", "04:24", "cancer"),
        ("2025-01-14", "09:12", "leo"),
        ("2025-01-16", "16:46", "virgo"),
    ]


@pytest.fixture
def sun_ophiuchus_dates():
    """
    IAU constellation boundary data for Ophiuchus.
    
    The Sun enters Ophiuchus around Nov 30 and exits around Dec 17.
    """
    return {
        "enters": "2025-11-30",
        "exits": "2025-12-17",
        "constellation": "ophiuchus",
    }


@pytest.fixture
def lahiri_ayanamsa_2025():
    """
    Lahiri ayanamsa value for 2025.
    
    Approximately 24° 18' (24.31°)
    """
    return 24.31


@pytest.fixture
def known_positions():
    """
    Known planetary positions on specific dates for verification.
    
    Format: {
        "date": {
            "planet": {
                "tropical": "sign",
                "sidereal": "sign",  # Lahiri
            }
        }
    }
    """
    return {
        "2025-06-15": {
            "jupiter": {
                "tropical": "cancer",
                "sidereal": "gemini",
            },
            "saturn": {
                "tropical": "aries",
                "sidereal": "pisces",
            },
        },
        "2024-01-01": {
            "jupiter": {
                "tropical": "taurus",
                "sidereal": "aries",
            },
        },
    }
