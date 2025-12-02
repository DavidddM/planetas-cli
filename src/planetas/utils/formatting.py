import json
import csv
import io
from typing import Sequence, Mapping

from ..models import DateRange, SignPosition, MultiSystemResult


def format_date_ranges_table(ranges: Sequence[DateRange], include_time: bool = False) -> str:
    """
    Format date ranges as a human-readable table.

    Args:
        ranges: Sequence of DateRange objects.
        include_time: Whether to include time in output.

    Returns:
        Formatted table string.
    """
    if not ranges:
        return "No ranges found."

    lines = []
    header = "Start" + " " * 12 + "End" + " " * 14 + "Duration (days)"
    lines.append(header)
    lines.append("-" * len(header))

    for r in ranges:
        start = r.format_start(include_time)
        end = r.format_end(include_time)
        duration = f"{r.duration_days:.1f}"
        lines.append(f"{start:<17} {end:<17} {duration:>10}")

    lines.append("-" * len(header))
    lines.append(f"Total ranges: {len(ranges)}")

    return "\n".join(lines)


def _range_to_dict(r: DateRange, include_time: bool) -> dict:
    """Convert a DateRange to a dict for JSON/CSV output."""
    return {
        "start_date": r.start_date,
        "start_time": r.start_time if include_time else None,
        "end_date": r.end_date,
        "end_time": r.end_time if include_time else None,
        "sign": r.sign.display_name,
        "duration_days": round(r.duration_days, 2),
    }


def format_date_ranges_json(ranges: Sequence[DateRange], include_time: bool = False) -> str:
    """
    Format date ranges as JSON.

    Args:
        ranges: Sequence of DateRange objects.
        include_time: Whether to include time in output.

    Returns:
        JSON string.
    """
    data = [_range_to_dict(r, include_time) for r in ranges]
    return json.dumps(data, indent=2)


def format_date_ranges_csv(ranges: Sequence[DateRange], include_time: bool = False) -> str:
    """
    Format date ranges as CSV.

    Args:
        ranges: Sequence of DateRange objects.
        include_time: Whether to include time in output.

    Returns:
        CSV string.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["start_date", "start_time", "end_date", "end_time", "sign", "duration_days"])

    for r in ranges:
        d = _range_to_dict(r, include_time)
        writer.writerow([
            d["start_date"],
            d["start_time"] or "",
            d["end_date"],
            d["end_time"] or "",
            d["sign"],
            d["duration_days"],
        ])

    return output.getvalue()


def format_sign_result(result: SignPosition, system_name: str) -> str:
    """
    Format a single sign position result.

    Args:
        result: SignPosition object.
        system_name: Name of the zodiac system.

    Returns:
        Formatted string.
    """
    sign_name = result.sign.display_name
    longitude_str = result.format_longitude(precision=2)

    if result.longitude_in_sign is not None:
        degrees = int(result.longitude_in_sign)
        minutes = int((result.longitude_in_sign - degrees) * 60)
        position_in_sign = f"{degrees}°{minutes:02d}'"
        return f"{system_name}: {sign_name} ({position_in_sign} in sign, {longitude_str} absolute)"

    return f"{system_name}: {sign_name} ({longitude_str})"


def format_multi_system_result(
    result: MultiSystemResult,
    ayanamsa_name: str | None = None,
) -> str:
    """
    Format a multi-system result for display.

    Args:
        result: MultiSystemResult object.
        ayanamsa_name: Name of the ayanamsa used for sidereal calculations.

    Returns:
        Formatted multi-line string.
    """
    lines = [f"Date: {result.date.strftime('%Y-%m-%d %H:%M:%S UTC')}"]
    lines.append("")

    if result.tropical:
        lines.append(format_sign_result(result.tropical, "Tropical"))
    if result.sidereal:
        sidereal_label = f"Sidereal ({ayanamsa_name})" if ayanamsa_name else "Sidereal"
        lines.append(format_sign_result(result.sidereal, sidereal_label))
    if result.astronomical:
        lines.append(format_sign_result(result.astronomical, "Astronomical"))

    return "\n".join(lines)


def format_multi_system_ranges_table(
    ranges_by_system: Mapping[str, Sequence[DateRange]],
    include_time: bool = False,
) -> str:
    """
    Format date ranges from multiple systems as a human-readable table.

    Args:
        ranges_by_system: Dict mapping system name to list of DateRange objects.
        include_time: Whether to include time in output.

    Returns:
        Formatted table string.
    """
    lines = []

    for system_name, ranges in ranges_by_system.items():
        if lines:
            lines.append("")

        lines.append(f"=== {system_name} ===")

        if not ranges:
            lines.append("No ranges found.")
            continue

        header = "Start" + " " * 12 + "End" + " " * 14 + "Duration (days)"
        lines.append(header)
        lines.append("-" * len(header))

        for r in ranges:
            start = r.format_start(include_time)
            end = r.format_end(include_time)
            duration = f"{r.duration_days:.1f}"
            lines.append(f"{start:<17} {end:<17} {duration:>10}")

        lines.append("-" * len(header))
        lines.append(f"Total ranges: {len(ranges)}")

    return "\n".join(lines)


def format_multi_system_ranges_json(
    ranges_by_system: Mapping[str, Sequence[DateRange]],
    include_time: bool = False,
) -> str:
    """
    Format date ranges from multiple systems as JSON.

    Args:
        ranges_by_system: Dict mapping system name to list of DateRange objects.
        include_time: Whether to include time in output.

    Returns:
        JSON string.
    """
    data = {}
    for system_name, ranges in ranges_by_system.items():
        data[system_name] = [_range_to_dict(r, include_time) for r in ranges]
    return json.dumps(data, indent=2)


def format_multi_system_ranges_csv(
    ranges_by_system: Mapping[str, Sequence[DateRange]],
    include_time: bool = False,
) -> str:
    """
    Format date ranges from multiple systems as CSV.

    Args:
        ranges_by_system: Dict mapping system name to list of DateRange objects.
        include_time: Whether to include time in output.

    Returns:
        CSV string.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["system", "start_date", "start_time", "end_date", "end_time", "sign", "duration_days"])

    for system_name, ranges in ranges_by_system.items():
        for r in ranges:
            d = _range_to_dict(r, include_time)
            writer.writerow([
                system_name,
                d["start_date"],
                d["start_time"] or "",
                d["end_date"],
                d["end_time"] or "",
                d["sign"],
                d["duration_days"],
            ])

    return output.getvalue()
