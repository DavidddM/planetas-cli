from enum import IntEnum


class Planet(IntEnum):
    """
    Celestial bodies supported by the calculator.

    Values correspond to Swiss Ephemeris planet constants.
    """

    SUN = 0
    MOON = 1
    MERCURY = 2
    VENUS = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8
    PLUTO = 9

    @property
    def display_name(self) -> str:
        """Return human-readable name."""
        names = {
            Planet.SUN: "Sun",
            Planet.MOON: "Moon",
            Planet.MERCURY: "Mercury",
            Planet.VENUS: "Venus",
            Planet.MARS: "Mars",
            Planet.JUPITER: "Jupiter",
            Planet.SATURN: "Saturn",
            Planet.URANUS: "Uranus",
            Planet.NEPTUNE: "Neptune",
            Planet.PLUTO: "Pluto",
        }
        return names[self]

    @property
    def search_step_days(self) -> int:
        """
        Return optimal coarse search step size in days.

        Based on typical orbital period and sign transit duration.
        Smaller values for faster-moving bodies.
        """
        steps = {
            Planet.SUN: 7,
            Planet.MOON: 1,
            Planet.MERCURY: 5,
            Planet.VENUS: 7,
            Planet.MARS: 14,
            Planet.JUPITER: 30,
            Planet.SATURN: 30,
            Planet.URANUS: 90,
            Planet.NEPTUNE: 90,
            Planet.PLUTO: 90,
        }
        return steps[self]

    @classmethod
    def from_string(cls, name: str) -> "Planet":
        """
        Parse planet from string input.

        Accepts: full name, lowercase.
        Raises ValueError if not found.
        """
        normalized = name.lower().strip()
        aliases = {
            "sun": cls.SUN,
            "moon": cls.MOON,
            "mercury": cls.MERCURY,
            "venus": cls.VENUS,
            "mars": cls.MARS,
            "jupiter": cls.JUPITER,
            "saturn": cls.SATURN,
            "uranus": cls.URANUS,
            "neptune": cls.NEPTUNE,
            "pluto": cls.PLUTO,
        }
        if normalized not in aliases:
            valid = ", ".join(sorted(set(aliases.keys())))
            raise ValueError(f"Unknown planet: {name}. Valid options: {valid}")
        return aliases[normalized]
