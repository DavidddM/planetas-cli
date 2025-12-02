from enum import IntEnum


class Ayanamsa(IntEnum):
    """
    Ayanamsa systems for sidereal zodiac calculations.

    Values correspond to Swiss Ephemeris SIDM_* constants.
    """

    LAHIRI = 1
    FAGAN_BRADLEY = 0
    RAMAN = 3
    KRISHNAMURTI = 5
    YUKTESHWAR = 7
    JN_BHASIN = 8
    DELUCE = 2
    SASSANIAN = 16
    GALACTIC_CENTER_0SAG = 17
    TRUE_CITRA = 27
    TRUE_REVATI = 28
    TRUE_PUSHYA = 29

    @property
    def display_name(self) -> str:
        """Return human-readable name."""
        names = {
            Ayanamsa.LAHIRI: "Lahiri (Indian Standard)",
            Ayanamsa.FAGAN_BRADLEY: "Fagan-Bradley (Western Sidereal)",
            Ayanamsa.RAMAN: "Raman",
            Ayanamsa.KRISHNAMURTI: "Krishnamurti",
            Ayanamsa.YUKTESHWAR: "Yukteshwar",
            Ayanamsa.JN_BHASIN: "JN Bhasin",
            Ayanamsa.DELUCE: "De Luce",
            Ayanamsa.SASSANIAN: "Sassanian",
            Ayanamsa.GALACTIC_CENTER_0SAG: "Galactic Center 0° Sagittarius",
            Ayanamsa.TRUE_CITRA: "True Chitra",
            Ayanamsa.TRUE_REVATI: "True Revati",
            Ayanamsa.TRUE_PUSHYA: "True Pushya",
        }
        return names[self]

    @classmethod
    def from_string(cls, name: str) -> "Ayanamsa":
        """
        Parse ayanamsa from string input.

        Accepts: full name, lowercase, common aliases.
        Raises ValueError if not found.
        """
        normalized = name.lower().strip().replace("-", "_").replace(" ", "_")
        aliases = {
            "lahiri": cls.LAHIRI,
            "fagan_bradley": cls.FAGAN_BRADLEY,
            "fagan": cls.FAGAN_BRADLEY,
            "bradley": cls.FAGAN_BRADLEY,
            "raman": cls.RAMAN,
            "krishnamurti": cls.KRISHNAMURTI,
            "kp": cls.KRISHNAMURTI,
            "yukteshwar": cls.YUKTESHWAR,
            "jn_bhasin": cls.JN_BHASIN,
            "bhasin": cls.JN_BHASIN,
            "deluce": cls.DELUCE,
            "de_luce": cls.DELUCE,
            "sassanian": cls.SASSANIAN,
            "galactic_center_0sag": cls.GALACTIC_CENTER_0SAG,
            "galactic": cls.GALACTIC_CENTER_0SAG,
            "true_citra": cls.TRUE_CITRA,
            "citra": cls.TRUE_CITRA,
            "true_revati": cls.TRUE_REVATI,
            "revati": cls.TRUE_REVATI,
            "true_pushya": cls.TRUE_PUSHYA,
            "pushya": cls.TRUE_PUSHYA,
        }
        if normalized not in aliases:
            valid = ", ".join(sorted(set(aliases.keys())))
            raise ValueError(f"Unknown ayanamsa: {name}. Valid options: {valid}")
        return aliases[normalized]
