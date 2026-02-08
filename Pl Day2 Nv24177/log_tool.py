"""
PL202 — Day 2 (45 min) — Log Filter CLI Tool (Individual)
"""

import argparse
from pathlib import Path

LOG_FILE = Path("logs.txt")
DEFAULT_OUT = "filtered_logs.txt"
ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}


def parse_line(line: str):
    """
    Parse a log line.
    Returns (timestamp, level, service, message) OR None if invalid format.
    """
    line = line.strip()
    if not line:
        return None

    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 4:
        return None

    timestamp, level, service, message = parts
    return timestamp, level, service, message


def is_valid_level(level: str) -> bool:
    """Return True if level is one of INFO/WARN/ERROR."""
    return level.upper() in ALLOWED_LEVELS


def matches_filters(level: str, service: str, level_filter, service_filter) -> bool:
    """Return True if the line matches the provided filters."""
    if level_filter and level.upper() != level_filter:
        return False
    if service_filter and service != service_filter:
        return False
    return True


def build_arg_parser() -> argparse.ArgumentParser:
    """Create and return the argparse parser."""
    parser = argparse.ArgumentParser(description="Filter cloud logs by level and/or service.")
    parser.add_argument("--level", help="Filter by log level (INFO, WARN, ERROR)", type=str)
    parser.add_argument("--service", help="Filter by service name", type=str)
    parser.add_argument("--out", help="Output filename", default=DEFAULT_OUT)
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    level_filter = args.level.upper() if args.level else None
    service_filter = args.service if args.service else None
    out_path = Path(args.out)

    if not LOG_FILE.exists():
        print(f"ERROR: Cannot find {LOG_FILE}. Put logs.txt in the same folder as this file.")
        return

    total_valid_scanned = 0
    lines_written = 0
    output_lines = []

    with open(LOG_FILE, "r", encoding="utf-8") as infile:
        for line in infile:
            parsed = parse_line(line)
            if not parsed:
                continue

            timestamp, level, service, message = parsed
            level = level.upper()

            if not is_valid_level(level):
                continue

            total_valid_scanned += 1

            if matches_filters(level, service, level_filter, service_filter):
                output_lines.append(f"{timestamp} | {level} | {service} | {message}")
                lines_written += 1

    with open(out_path, "w", encoding="utf-8") as outfile:
        for line in output_lines:
            outfile.write(line + "\n")

    print(f"Valid lines scanned: {total_valid_scanned}")
    print(f"Lines written: {lines_written}")
    print(f"Output file: {out_path}")


if __name__ == "__main__":
    main()
