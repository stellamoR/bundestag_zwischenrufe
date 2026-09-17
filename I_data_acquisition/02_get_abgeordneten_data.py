"""Create the Bundestag member/party lookup CSV from MDB_STAMMDATEN.XML."""

from __future__ import annotations

import argparse
import csv
import xml.etree.ElementTree as ET
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "_data"
DEFAULT_XML = DATA_DIR / "MDB_STAMMDATEN.XML"
DEFAULT_OUTPUT = DATA_DIR / "abgeordnete.csv"

# Government members and other speakers absent from the XML-derived lookup.
MANUAL_ENTRIES = [
    ("Boris Pistorius", "SPD", "20"),
    ("Nancy Faeser", "SPD", "20"),
    ("Klaus-Dieter Fritsche", "CDU/CSU", "19"),
    ("Aydan Özoguz", "SPD", "19"),
    ("Johanna Wanka", "CDU/CSU", "18"),
    ("Philipp Rösler", "FDP", "17"),
    ("Hans-Jürgen Beerfeltz", "FDP", "17"),
    ("Erich Stather", "SPD", "16"),
    ("Wolfgang Clement", "SPD", "14"),
    ("Christina Weiss", "fraktionslos", "14"),
    ("Julian Nida-Rümelin", "SPD", "14"),
    ("Michael Naumann", "SPD", "14"),
    ("Werner Tegtmeier", "SPD", "13"),
    ("Jürgen Stark", "fraktionslos", "13"),
    ("Hans-Friedrich von Ploetz", "fraktionslos", "13"),
    ("Baldur Wagner", "CDU/CSU", "12"),
    ("Karl Jung", "fraktionslos", "12"),
    ("Franz-Josef Feiter", "fraktionslos", "12"),
    ("Manfred Overhaus", "fraktionslos", "12"),
    ("Wighard Härdtl", "CDU/CSU", "12"),
    ("Wilhelm Knittel", "CDU/CSU", "12"),
    ("Clemens Stroetmann", "CDU/CSU", "12"),
    ("Franz Kroppenstedt", "CDU/CSU", "12"),
    ("Hans-Joachim Fuchtel", "CDU/CSU", "12"),
    ("Frerich Görts", "CDU/CSU", "12"),
]


def member_rows(xml_path: Path) -> list[tuple[str, str, str]]:
    """Extract all distinct name variants with party and latest election period."""
    root = ET.parse(xml_path).getroot()
    rows: list[tuple[str, str, str]] = []

    for member in root.findall("MDB"):
        periods = member.findall(".//WAHLPERIODE")
        if not periods:
            continue
        period_element = periods[-1].find("WP")
        if period_element is None or period_element.text is None:
            continue
        period = period_element.text
        party = member.findtext(".//PARTEI_KURZ", default="<unknown>")
        if party in {"BÜNDNIS 90/DIE GRÜNEN", "DIE GRÜNEN/BÜNDNIS 90"}:
            party = "GRÜNE"

        processed_names: set[str] = set()
        for name_element in member.findall(".//NAME"):
            first_name = name_element.findtext("VORNAME")
            last_name = name_element.findtext("NACHNAME")
            if not first_name or not last_name:
                continue
            full_name = f"{first_name} {last_name}"
            if full_name in processed_names:
                continue

            # Add both "Lutz G. Stavenhagen" and "Lutz Stavenhagen" for old data.
            if first_name.endswith(".") and int(period) < 18:
                rows.append((full_name, party, period))
                abbreviated_parts = first_name.split()
                if len(abbreviated_parts) > 1:
                    first_name = " ".join(abbreviated_parts[:-1])

            rows.append((f"{first_name} {last_name}", party, period))
            processed_names.add(full_name)

    rows.extend(MANUAL_ENTRIES)
    return sorted(rows, key=lambda row: int(row[2]), reverse=True)


def write_member_csv(xml_path: Path = DEFAULT_XML, output_path: Path = DEFAULT_OUTPUT) -> int:
    rows = member_rows(xml_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["name", "party", "BT-Period"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} entries to {output_path}")
    return len(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xml", type=Path, default=DEFAULT_XML)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    write_member_csv(arguments.xml, arguments.output)
