import sys
from datetime import datetime
from pathlib import Path

import click

from .config import Config
from .core import TropicalCalculator, SiderealCalculator, AstronomicalCalculator
from .models import Planet, ZodiacSign, Constellation, Ayanamsa, MultiSystemResult
from .search import RangeFinder
from .utils import (
    parse_date,
    format_date_ranges_table,
    format_date_ranges_json,
    format_date_ranges_csv,
    format_multi_system_result,
    format_multi_system_ranges_table,
    format_multi_system_ranges_json,
    format_multi_system_ranges_csv,
)


@click.group()
@click.option(
    "--ephe-path",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Path to Swiss Ephemeris data files.",
)
@click.option(
    "--precision",
    type=click.Choice(["day", "minute"]),
    default="day",
    help="Output precision level.",
)
@click.pass_context
def main(ctx: click.Context, ephe_path: Path | None, precision: str) -> None:
    """
    Planetas - Planetary zodiac position calculator.

    Calculate positions in tropical, sidereal, and astronomical (IAU) systems.

    \b
    Examples:
      planetas sign -p jupiter -d 2025-06-15
      planetas ranges -p saturn -g aquarius -s 2000-01-01 -e 2030-12-31

    \b
    Environment:
      SWISSEPH_PATH   Path to ephemeris data files (or use --ephe-path)
    """
    ctx.ensure_object(dict)

    if ephe_path:
        Config.set_ephemeris_path(ephe_path)

    Config.set_precision_minutes(precision == "minute")
    ctx.obj["include_time"] = precision == "minute"


@main.command()
@click.option(
    "--planet", "-p",
    required=True,
    help="Planet name (sun, moon, mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto).",
)
@click.option(
    "--date", "-d",
    required=True,
    help="Date to query in UTC (YYYY-MM-DD or YYYY-MM-DD HH:MM).",
)
@click.option(
    "--system", "-s",
    type=click.Choice(["tropical", "sidereal", "astronomical", "all"]),
    default="all",
    help="Zodiac system to use.",
)
@click.option(
    "--ayanamsa", "-a",
    default="lahiri",
    help="Ayanamsa for sidereal calculations (lahiri, fagan_bradley, raman, etc.).",
)
def sign(
    planet: str,
    date: str,
    system: str,
    ayanamsa: str,
) -> None:
    """
    Get which zodiac sign a planet occupies on a date.

    \b
    Examples:
      planetas sign -p jupiter -d 2025-06-15
      planetas sign -p mars -d "2025-01-01 12:00" -s sidereal
      planetas sign -p moon -d today -s tropical
    """
    try:
        planet_enum = Planet.from_string(planet)
        query_date = parse_date(date)
        ayanamsa_enum = Ayanamsa.from_string(ayanamsa)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    tropical_result = None
    sidereal_result = None
    astronomical_result = None

    try:
        if system in ("tropical", "all"):
            calc = TropicalCalculator()
            tropical_result = calc.get_sign(planet_enum, query_date)

        if system in ("sidereal", "all"):
            calc = SiderealCalculator(ayanamsa_enum)
            sidereal_result = calc.get_sign(planet_enum, query_date)

        if system in ("astronomical", "all"):
            calc = AstronomicalCalculator()
            astronomical_result = calc.get_sign(planet_enum, query_date)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    result = MultiSystemResult(
        tropical=tropical_result,
        sidereal=sidereal_result,
        astronomical=astronomical_result,
        date=query_date,
    )

    click.echo(f"\n{planet_enum.display_name} position:")
    click.echo(format_multi_system_result(result, ayanamsa_enum.display_name))


def _parse_sign_for_system(sign_str: str, system: str) -> ZodiacSign | Constellation:
    """
    Parse a sign string for a specific system.

    For astronomical system, parses as Constellation.
    For tropical/sidereal, parses as ZodiacSign.
    """
    if system == "astronomical":
        return Constellation.from_string(sign_str)
    return ZodiacSign.from_string(sign_str)


def _run_range_search(
    planet: Planet,
    sign_str: str,
    start_date: datetime,
    end_date: datetime,
    system: str,
    ayanamsa: Ayanamsa,
) -> tuple[str, list]:
    """
    Run a range search for a single system.

    Returns tuple of (system_display_name, list_of_ranges).
    """
    target_sign = _parse_sign_for_system(sign_str, system)

    if system == "tropical":
        calculator = TropicalCalculator()
    elif system == "sidereal":
        calculator = SiderealCalculator(ayanamsa)
    else:
        calculator = AstronomicalCalculator()

    finder = RangeFinder(calculator)
    ranges = list(finder.find_ranges(planet, target_sign, start_date, end_date))

    return calculator.system_name, ranges


@main.command()
@click.option(
    "--planet", "-p",
    required=True,
    help="Planet name.",
)
@click.option(
    "--sign", "-g",
    required=True,
    help="Target zodiac sign or constellation.",
)
@click.option(
    "--start", "-s",
    required=True,
    help="Start date of search range in UTC (YYYY-MM-DD).",
)
@click.option(
    "--end", "-e",
    required=True,
    help="End date of search range in UTC (YYYY-MM-DD).",
)
@click.option(
    "--system",
    type=click.Choice(["tropical", "sidereal", "astronomical", "all"]),
    default="all",
    help="Zodiac system to use.",
)
@click.option(
    "--ayanamsa", "-a",
    default="lahiri",
    help="Ayanamsa for sidereal calculations.",
)
@click.option(
    "--format", "-f",
    "output_format",
    type=click.Choice(["table", "json", "csv"]),
    default="table",
    help="Output format.",
)
@click.option(
    "--output", "-o",
    type=click.Path(path_type=Path),
    default=None,
    help="Output file path. If not specified, prints to stdout.",
)
@click.pass_context
def ranges(
    ctx: click.Context,
    planet: str,
    sign: str,
    start: str,
    end: str,
    system: str,
    ayanamsa: str,
    output_format: str,
    output: Path | None,
) -> None:
    """
    Find all date ranges when a planet was in a sign.

    \b
    Examples:
      planetas ranges -p jupiter -g aquarius -s 2000-01-01 -e 2030-12-31
      planetas ranges -p saturn -g capricorn -s 1900-01-01 -e 2100-12-31 --system sidereal
      planetas ranges -p moon -g cancer -s 2025-01-01 -e 2025-12-31 -f json
      planetas ranges -p mars -g aries -s 2020-01-01 -e 2025-12-31 -f csv -o results.csv
    """
    try:
        planet_enum = Planet.from_string(planet)
        start_date = parse_date(start)
        end_date = parse_date(end)
        ayanamsa_enum = Ayanamsa.from_string(ayanamsa)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if start_date >= end_date:
        click.echo("Error: Start date must be before end date.", err=True)
        sys.exit(1)

    if output and output_format == "table":
        click.echo(
            "Warning: Table format is not ideal for file output. "
            "Consider using --format json or --format csv.",
            err=True,
        )

    include_time = ctx.obj.get("include_time", False)

    try:
        if system == "all":
            if output_format == "table":
                click.echo(
                    f"\nSearching for {planet_enum.display_name} in {sign} "
                    f"(all systems)...",
                    err=True,
                )

            results_by_system = {}
            for sys_name in ["tropical", "sidereal", "astronomical"]:
                display_name, range_list = _run_range_search(
                    planet_enum, sign, start_date, end_date, sys_name, ayanamsa_enum
                )
                results_by_system[display_name] = range_list

            if output_format == "table":
                formatted = format_multi_system_ranges_table(results_by_system, include_time)
            elif output_format == "json":
                formatted = format_multi_system_ranges_json(results_by_system, include_time)
            else:
                formatted = format_multi_system_ranges_csv(results_by_system, include_time)

        else:
            display_name, results = _run_range_search(
                planet_enum, sign, start_date, end_date, system, ayanamsa_enum
            )

            if output_format == "table":
                click.echo(
                    f"\nSearching for {planet_enum.display_name} in {sign} "
                    f"({display_name})...",
                    err=True,
                )

            if output_format == "table":
                formatted = format_date_ranges_table(results, include_time)
            elif output_format == "json":
                formatted = format_date_ranges_json(results, include_time)
            else:
                formatted = format_date_ranges_csv(results, include_time)

        if output:
            output.write_text(formatted)
            click.echo(f"Results written to {output}", err=True)
        else:
            click.echo(formatted)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
def list_planets() -> None:
    """List all supported planets and celestial bodies."""
    click.echo("\nSupported planets:")
    click.echo("-" * 40)
    for planet in Planet:
        click.echo(f"  {planet.name.lower():<15} {planet.display_name}")


@main.command()
def list_signs() -> None:
    """List all zodiac signs and constellations."""
    click.echo("\nZodiac Signs (Tropical/Sidereal):")
    click.echo("-" * 40)
    for sign in ZodiacSign:
        click.echo(f"  {sign.name.lower():<15} {sign.longitude_start:>5.0f}° - {sign.longitude_end:>5.0f}°")

    click.echo("\n\nEcliptic Constellations (Astronomical):")
    click.echo("-" * 40)
    for const in Constellation:
        click.echo(f"  {const.name.lower():<15} ({const.abbreviation})")


@main.command()
def list_ayanamsas() -> None:
    """List all supported ayanamsa systems."""
    click.echo("\nSupported Ayanamsas:")
    click.echo("-" * 50)
    for ayan in Ayanamsa:
        click.echo(f"  {ayan.name.lower():<20} {ayan.display_name}")


if __name__ == "__main__":
    main()
