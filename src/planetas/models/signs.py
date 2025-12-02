from enum import IntEnum


class ZodiacSign(IntEnum):
    """
    Traditional 12-sign zodiac used in tropical and sidereal systems.

    Values represent the sign index (0-11), corresponding to 30-degree segments.
    """

    ARIES = 0
    TAURUS = 1
    GEMINI = 2
    CANCER = 3
    LEO = 4
    VIRGO = 5
    LIBRA = 6
    SCORPIO = 7
    SAGITTARIUS = 8
    CAPRICORN = 9
    AQUARIUS = 10
    PISCES = 11

    @property
    def display_name(self) -> str:
        """Return capitalized sign name."""
        return self.name.capitalize()

    @property
    def longitude_start(self) -> float:
        """Return starting longitude in degrees (0-360)."""
        return float(self.value * 30)

    @property
    def longitude_end(self) -> float:
        """Return ending longitude in degrees (exclusive)."""
        return float((self.value + 1) * 30)

    @classmethod
    def from_longitude(cls, longitude: float) -> "ZodiacSign":
        """
        Determine sign from ecliptic longitude.

        Args:
            longitude: Ecliptic longitude in degrees (0-360).

        Returns:
            ZodiacSign corresponding to that longitude.
        """
        normalized = longitude % 360
        index = int(normalized // 30)
        return cls(index)

    @classmethod
    def from_string(cls, name: str) -> "ZodiacSign":
        """
        Parse sign from string input.

        Accepts: full name, lowercase, common abbreviations.
        Raises ValueError if not found.
        """
        normalized = name.lower().strip()
        aliases = {
            "aries": cls.ARIES,
            "ari": cls.ARIES,
            "taurus": cls.TAURUS,
            "tau": cls.TAURUS,
            "gemini": cls.GEMINI,
            "gem": cls.GEMINI,
            "cancer": cls.CANCER,
            "can": cls.CANCER,
            "leo": cls.LEO,
            "virgo": cls.VIRGO,
            "vir": cls.VIRGO,
            "libra": cls.LIBRA,
            "lib": cls.LIBRA,
            "scorpio": cls.SCORPIO,
            "sco": cls.SCORPIO,
            "sagittarius": cls.SAGITTARIUS,
            "sag": cls.SAGITTARIUS,
            "capricorn": cls.CAPRICORN,
            "cap": cls.CAPRICORN,
            "aquarius": cls.AQUARIUS,
            "aqu": cls.AQUARIUS,
            "pisces": cls.PISCES,
            "pis": cls.PISCES,
        }
        if normalized not in aliases:
            valid = ", ".join(sorted(set(aliases.keys())))
            raise ValueError(f"Unknown sign: {name}. Valid options: {valid}")
        return aliases[normalized]


class Constellation(IntEnum):
    """
    The 13 constellations through which the ecliptic passes.

    Used for astronomical (IAU) zodiac positions.
    Values are arbitrary identifiers, not indices.
    """

    ARIES = 1
    TAURUS = 2
    GEMINI = 3
    CANCER = 4
    LEO = 5
    VIRGO = 6
    LIBRA = 7
    SCORPIUS = 8
    OPHIUCHUS = 9
    SAGITTARIUS = 10
    CAPRICORNUS = 11
    AQUARIUS = 12
    PISCES = 13

    @property
    def display_name(self) -> str:
        """Return constellation name."""
        return self.name.capitalize()

    @property
    def abbreviation(self) -> str:
        """Return official IAU 3-letter abbreviation."""
        abbrevs = {
            Constellation.ARIES: "Ari",
            Constellation.TAURUS: "Tau",
            Constellation.GEMINI: "Gem",
            Constellation.CANCER: "Cnc",
            Constellation.LEO: "Leo",
            Constellation.VIRGO: "Vir",
            Constellation.LIBRA: "Lib",
            Constellation.SCORPIUS: "Sco",
            Constellation.OPHIUCHUS: "Oph",
            Constellation.SAGITTARIUS: "Sgr",
            Constellation.CAPRICORNUS: "Cap",
            Constellation.AQUARIUS: "Aqr",
            Constellation.PISCES: "Psc",
        }
        return abbrevs[self]

    @classmethod
    def from_abbreviation(cls, abbrev: str) -> "Constellation | None":
        """
        Parse constellation from IAU abbreviation.

        Args:
            abbrev: 3-letter IAU abbreviation (case-insensitive).

        Returns:
            Matching Constellation, or None if not an ecliptic constellation.
        """
        normalized = abbrev.strip().capitalize()
        abbrev_map = {c.abbreviation: c for c in cls}
        return abbrev_map.get(normalized)

    @classmethod
    def from_string(cls, name: str) -> "Constellation":
        """
        Parse constellation from string input.

        Accepts: full name, lowercase, abbreviations.
        Raises ValueError if not found.
        """
        normalized = name.lower().strip()
        aliases = {
            "aries": cls.ARIES,
            "ari": cls.ARIES,
            "taurus": cls.TAURUS,
            "tau": cls.TAURUS,
            "gemini": cls.GEMINI,
            "gem": cls.GEMINI,
            "cancer": cls.CANCER,
            "cnc": cls.CANCER,
            "leo": cls.LEO,
            "virgo": cls.VIRGO,
            "vir": cls.VIRGO,
            "libra": cls.LIBRA,
            "lib": cls.LIBRA,
            "scorpius": cls.SCORPIUS,
            "scorpio": cls.SCORPIUS,
            "sco": cls.SCORPIUS,
            "ophiuchus": cls.OPHIUCHUS,
            "oph": cls.OPHIUCHUS,
            "sagittarius": cls.SAGITTARIUS,
            "sgr": cls.SAGITTARIUS,
            "sag": cls.SAGITTARIUS,
            "capricornus": cls.CAPRICORNUS,
            "capricorn": cls.CAPRICORNUS,
            "cap": cls.CAPRICORNUS,
            "aquarius": cls.AQUARIUS,
            "aqr": cls.AQUARIUS,
            "aqu": cls.AQUARIUS,
            "pisces": cls.PISCES,
            "psc": cls.PISCES,
            "pis": cls.PISCES,
        }
        if normalized not in aliases:
            valid = ", ".join(sorted(set(aliases.keys())))
            raise ValueError(f"Unknown constellation: {name}. Valid options: {valid}")
        return aliases[normalized]
