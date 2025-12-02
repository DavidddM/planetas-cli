# Planetas

Planetary zodiac position calculator supporting tropical, sidereal, and astronomical (IAU) coordinate systems.

## Features

- **Sign lookup**: Get which zodiac sign or constellation a planet occupies on any date
- **Date range search**: Find all periods when a planet was in a specific sign
- **Three zodiac systems**:
  - Tropical (Western astrology, anchored to vernal equinox)
  - Sidereal (Vedic astrology, with configurable ayanamsa)
  - Astronomical (IAU constellation boundaries, includes Ophiuchus)
- **Multiple output formats**: Table, JSON, CSV
- **Configurable precision**: Day-level or minute-level accuracy

## Installation

### 1. Install the package

```bash
git clone <repository-url>
cd planetas
pip install -e .
```

### 2. Swiss Ephemeris data files (optional)

Planetas uses the Swiss Ephemeris for planetary calculations. Without external data files, it uses the built-in **Moshier ephemeris** as a fallback.

#### Moshier vs JPL ephemeris

| | Moshier (built-in) | JPL files (.se1) |
|---|---|---|
| Accuracy | ~1 arc-second (Moon), few arc-seconds (planets) | Sub-arc-second |
| Date range | Any date | Depends on files installed |
| Setup | None required | Download files |

For most purposes, Moshier is sufficient. Install the JPL files if you need higher precision.

#### Installing ephemeris files

**Option A: Download all files (recommended)**

```bash
mkdir -p $HOME/.swisseph/ephe && cd $HOME/.swisseph/ephe
git clone --depth 1 --filter=blob:none --sparse https://github.com/aloistr/swisseph.git temp
cd temp && git sparse-checkout set ephe && mv ephe/* .. && cd .. && rm -rf temp
```

**Option B: Download specific files only**

```bash
mkdir -p $HOME/.swisseph/ephe && cd $HOME/.swisseph/ephe

# Main planetary ephemeris (1800 CE - 2400 CE)
curl -O https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1
curl -O https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1
```

#### Ephemeris file coverage

| File pattern | Coverage |
|--------------|----------|
| `sepl_18.se1`, `semo_18.se1` | 1800 CE - 2400 CE |
| `sepl_06.se1`, `semo_06.se1` | 600 CE - 1200 CE |
| `sepl_-06.se1`, `semo_-06.se1` | 600 BCE - 1 BCE |
| `sepl_m54.se1`, `semo_m54.se1` | 5400 BCE - 4800 BCE |

Files are named by the starting century. Download the files covering your date range of interest.

#### Configure ephemeris path

**Option 1: Environment variable (recommended)**

```bash
export SWISSEPH_PATH=$HOME/.swisseph/ephe
```

Add this to your shell configuration file to make it permanent:

```bash
# For bash
echo 'export SWISSEPH_PATH=$HOME/.swisseph/ephe' >> ~/.bashrc

# For zsh
echo 'export SWISSEPH_PATH=$HOME/.swisseph/ephe' >> ~/.zshrc
```

Then reload your shell or run `source ~/.bashrc` (or `~/.zshrc`).

**Option 2: CLI flag**

```bash
planetas --ephe-path /path/to/ephe sign -p jupiter -d 2025-06-15
```

**Option 3: Automatic detection**

Planetas searches these locations in order:
1. `SWISSEPH_PATH` environment variable
2. `$HOME/.swisseph/ephe`
3. `/usr/share/swisseph/ephe`
4. `/usr/local/share/swisseph/ephe`
5. `./ephe` (current directory)

## Usage

### Get planet position on a date

```bash
# All three systems (default)
planetas sign -p jupiter -d 2025-06-15

# Specific system
planetas sign -p mars -d "2025-01-01 12:00" -s sidereal

# With custom ayanamsa
planetas sign -p moon -d today -s sidereal -a fagan_bradley
```

Example output:
```
Jupiter position:
Date: 2025-06-15 00:00:00 UTC

Tropical: Cancer (0°42' in sign, 90°42'18.52" absolute)
Sidereal: Gemini (6°54' in sign, 66°54'22.31" absolute)
Astronomical: Gemini (90°42'18.52")
```

### Find date ranges

Find all periods when a planet occupied a specific sign:

```bash
# Table output (default)
planetas ranges -p jupiter -g aquarius -s 2000-01-01 -e 2030-12-31

# JSON output
planetas ranges -p saturn -g capricorn -s 2000-01-01 -e 2030-12-31 -f json

# CSV output to file
planetas ranges -p mars -g aries -s 2020-01-01 -e 2025-12-31 -f csv -o results.csv

# Specific system only
planetas ranges -p moon -g cancer -s 2025-01-01 -e 2025-12-31 --system tropical
```

### Minute-level precision

For more precise entry/exit times:

```bash
planetas --precision minute ranges -p venus -g taurus -s 2025-01-01 -e 2025-12-31
```

### List available options

```bash
planetas list-planets      # Show supported celestial bodies
planetas list-signs        # Show zodiac signs and constellations
planetas list-ayanamsas    # Show available ayanamsa systems
```

### Help

```bash
planetas --help
planetas sign --help
planetas ranges --help
```

## Configuration

### Environment variables

| Variable | Description |
|----------|-------------|
| `SWISSEPH_PATH` | Path to Swiss Ephemeris data files |

### Precision options

| Option | Description |
|--------|-------------|
| `--precision day` | Day-level precision (default) |
| `--precision minute` | Minute-level precision for sign ingress/egress times |

### Ayanamsa systems

For sidereal calculations, the following ayanamsa systems are supported:

| Name | Description |
|------|-------------|
| `lahiri` | Lahiri (Indian Standard) - default |
| `fagan_bradley` | Fagan-Bradley (Western Sidereal) |
| `raman` | Raman |
| `krishnamurti` | Krishnamurti (KP) |
| `true_citra` | True Chitra |
| `true_revati` | True Revati |
| `true_pushya` | True Pushya |

Use `planetas list-ayanamsas` for the complete list.

## Supported bodies

### Planets

Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto

### Zodiac signs (tropical/sidereal)

Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces

### Constellations (astronomical)

Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpius, Ophiuchus, Sagittarius, Capricornus, Aquarius, Pisces

## Technical notes

- All dates are interpreted as UTC
- Tropical zodiac is anchored to the vernal equinox (0° Aries = March equinox)
- Sidereal zodiac applies ayanamsa offset from tropical positions
- Astronomical positions use IAU constellation boundaries via Skyfield
- Planetary positions are geocentric (Earth-centered)

## Current limitations

- **BCE dates not supported**: Negative years (e.g., `-500`) are interpreted as positive years (500 CE)

## License

GPL-3.0 - See [LICENSE](LICENSE) for details.
