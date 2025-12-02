# Planetas Test Suite

Integration tests for the planetas CLI tool using verified astronomical data.

## Setup

```bash
cd /path/to/planetas
pip install -e ".[test]"
# or if no test extras defined:
pip install pytest
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_cli.py -v

# Run specific test
pytest tests/test_cli.py::test_jupiter_aquarius_ingress_2020 -v

# Run with output visible (useful for debugging)
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -v -x
```

## Test Data Sources

All test fixtures are derived from:
- Cafe Astrology (Swiss Ephemeris based)
- Siddhantika ephemeris tables
- Moontracks lunar ingress data
- EarthSky IAU constellation data

Times verified across multiple sources with typical agreement within 1-2 minutes.
