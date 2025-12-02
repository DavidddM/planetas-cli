from pathlib import Path
import os


class Config:
    """
    Global configuration for planetas.

    Ephemeris path resolution order:
    1. Explicitly set path via set_ephemeris_path()
    2. SWISSEPH_PATH environment variable
    3. ~/.swisseph/ephe
    4. /usr/share/swisseph/ephe
    5. /usr/local/share/swisseph/ephe
    6. ./ephe (current directory)
    """

    _ephemeris_path: Path | None = None
    _precision_minutes: bool = False

    @classmethod
    def get_ephemeris_path(cls) -> Path:
        """
        Return the configured ephemeris file path.

        Returns:
            Path to directory containing Swiss Ephemeris data files.

        Raises:
            FileNotFoundError: If no valid ephemeris path found.
        """
        if cls._ephemeris_path is not None:
            return cls._ephemeris_path

        env_path = os.environ.get("SWISSEPH_PATH")
        if env_path:
            path = Path(env_path)
            if path.is_dir():
                return path

        candidates = [
            Path.home() / ".swisseph" / "ephe",
            Path("/usr/share/swisseph/ephe"),
            Path("/usr/local/share/swisseph/ephe"),
            Path.cwd() / "ephe",
            Path.cwd(),
        ]

        for candidate in candidates:
            if candidate.is_dir():
                se1_files = list(candidate.glob("*.se1"))
                if se1_files:
                    return candidate

        raise FileNotFoundError(
            "No Swiss Ephemeris data files found. "
            "Set SWISSEPH_PATH environment variable or use --ephe-path option."
        )

    @classmethod
    def set_ephemeris_path(cls, path: Path) -> None:
        """Set the ephemeris file path explicitly."""
        if not path.is_dir():
            raise NotADirectoryError(f"Ephemeris path is not a directory: {path}")
        cls._ephemeris_path = path

    @classmethod
    def get_precision_minutes(cls) -> bool:
        """Return whether minute-level precision is enabled."""
        return cls._precision_minutes

    @classmethod
    def set_precision_minutes(cls, enabled: bool) -> None:
        """Enable or disable minute-level precision."""
        cls._precision_minutes = enabled
