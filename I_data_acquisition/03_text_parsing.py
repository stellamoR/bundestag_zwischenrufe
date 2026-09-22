"""Parse Bundestag protocol JSON files and build speech/interruption CSV files."""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from tqdm import tqdm


DATA_DIR = Path(__file__).resolve().parents[1] / "_data"
DEFAULT_PROTOCOLS = DATA_DIR / "protocols"
DEFAULT_PARSED = DATA_DIR / "parsed_protocols"
DEFAULT_MEMBERS = DATA_DIR / "abgeordnete.csv"
DEFAULT_MEMBERS_XML = DATA_DIR / "MDB_STAMMDATEN.XML"

PARTIES = ["CDU/CSU", "GRÜNE", "SPD", "FDP", "AfD", "DIE LINKE", "fraktionslos"]
PARTY_PATTERN = r"(CDU\/CSU|CSU|CDU|GRÜNE|FDP|AfD|SPD|DIE LINKE|fraktionslos)"
LEGACY_NAME_PATTERN = (
    r"((?:Dr\.\s)?(?:\w+(?:-\w+)?\s)(?:\w+\.\s)?(?:von\s)?\w+(?:-\w+)?)"
)

# These patterns intentionally recognize structure, not names. The text before
# each suffix is resolved against members recorded for the protocol's period.
SPEECH_SUFFIX_PATTERN = re.compile(
    rf"(?P<location>\([^()\r]{{1,60}}\)(?P<location_gap>\s*))?"
    rf"\((?P<party>{PARTY_PATTERN})\)(?P<pre_colon>[ \t\u00a0]*):"
    rf"(?P<post_colon>[ \t\u00a0\r\n]*)",
    flags=re.UNICODE,
)
INTERRUPTION_SUFFIX_PATTERN = re.compile(
    rf"(?P<location>\[[^\]\r]{{1,60}}\](?P<location_gap>\s*))?"
    rf"\[(?P<party>{PARTY_PATTERN})\](?P<pre_colon>[ \t\u00a0]*):"
    rf"(?P<post_colon>[ \t\u00a0\r\n]*)",
    flags=re.UNICODE,
)
INTERRUPTION_END_PATTERN = re.compile(r"[-–—\)]\s", flags=re.UNICODE)
CALLOUT_PATTERN = re.compile(
    r"[-–—\s\(]Zuruf .*?" rf"{PARTY_PATTERN}:\s" r"([\s\S]*?)[-–—\)]\s",
    flags=re.UNICODE,
)
# Some annotations identify a caller but do not transcribe anything said, for
# example ``(Zuruf der Abg. Sonja Lemke [DIE LINKE])``.  Keep the complete
# parenthetical here; names inside it are resolved against the period roster.
CALLER_ONLY_ZURUF_PATTERN = re.compile(
    r"\([^()\r]{0,500}\bZurufe?\b[^()\r]{0,500}\)",
    flags=re.UNICODE,
)
CALLER_ONLY_PARTY_PATTERN = re.compile(
    rf"\[(?P<bracket_party>{PARTY_PATTERN})\]|(?P<plain_party>{PARTY_PATTERN})",
    flags=re.UNICODE,
)
APPLAUSE_PATTERN = re.compile(
    r"[-–—\s\(]Beifall[\s\S]*?[-–—\)]",
    flags=re.UNICODE,
)
OFFICIAL_SPEAKER_PATTERN = re.compile(
    r"\n"
    rf"{LEGACY_NAME_PATTERN}, "
    r"((?:Parl\. Staatssekretär|Staatssekretär|Bundeskanzler|Bundesminister))"
    r"[\w ]{0,100}\n?[\w ]{0,100}?:",
    flags=re.UNICODE,
)
SPEECH_END_PATTERN = re.compile(r"(\nVizepräs.{0,99}?:)|(\nPräsid.{0,99}?:)|(\nAnlage)")


def load_members(path: Path) -> list[tuple[str, str, str]]:
    with path.open("r", encoding="utf-8", newline="") as input_file:
        reader = csv.reader(input_file)
        next(reader)
        return [tuple(row) for row in reader]  # type: ignore[list-item]


def find_party_by_name(name: str, members: Iterable[tuple[str, str, str]]) -> str:
    """Find a speaker's party, preferring the most recent membership record."""
    if name.startswith("Dr."):
        name = name[4:]
    for member_name, party, _period in sorted(
        members, key=lambda item: int(item[2]), reverse=True
    ):
        if name in member_name:
            return "CDU/CSU" if party in {"CDU", "CSU"} else party
    return "<unknown>"


def normalize(value: str) -> str:
    value = (
        unicodedata.normalize("NFKC", value)
        .replace("\u00a0", " ")
        .replace("\u00ad", "")
    )
    return " ".join(value.split()).strip()


def normalize_party(value: str) -> str | None:
    upper = normalize(value).upper()
    if "CHRISTLICH DEMOKRAT" in upper or "CHRISTLICH - SOZIAL" in upper or upper in {"CDU", "CSU", "CDU/CSU"}:
        return "CDU/CSU"
    if "SOZIALDEMOKRAT" in upper or upper == "SPD":
        return "SPD"
    if "BÜNDNIS 90" in upper or "GRÜNEN" in upper or upper == "GRÜNE":
        return "GRÜNE"
    if "FREIE DEMOKRAT" in upper or upper == "FDP":
        return "FDP"
    if "DIE LINKE" in upper or "PDS" in upper:
        return "DIE LINKE"
    if "ALTERNATIVE FÜR DEUTSCHLAND" in upper or upper == "AFD":
        return "AfD"
    if "FRAKTIONSLOS" in upper:
        return "fraktionslos"
    return None


def xml_name_variants(element: ET.Element) -> set[str]:
    """Build protocol-style names from the XML's separated name components."""
    first = normalize(element.findtext("VORNAME", ""))
    last = normalize(element.findtext("NACHNAME", ""))
    if not first or not last:
        return set()
    prefix = normalize(element.findtext("PRAEFIX", ""))
    nobility = normalize(element.findtext("ADEL", ""))
    nobility_variants = {nobility} if nobility else set()
    # The XML contains both abbreviated and written-out forms, while protocols
    # overwhelmingly spell these titles out.
    nobility_expansions = {"Frhr.": "Freiherr", "Frfr.": "Freifrau"}
    if nobility in nobility_expansions:
        nobility_variants.add(nobility_expansions[nobility])

    first_variants = {first}
    first_word = first.split()[0]
    first_variants.add(first_word)
    if "-" in first_word:
        first_variants.add(first_word.split("-", 1)[0])

    last_variants = {last}
    if "-" in last:
        last_variants.add(last.split("-", 1)[0])

    middle_variants = {""}
    if prefix:
        middle_variants.add(prefix)
    middle_variants.update(nobility_variants)
    for title in nobility_variants:
        if prefix:
            middle_variants.add(f"{title} {prefix}")
    return {
        normalize(" ".join(part for part in (first_name, middle, last_name) if part))
        for first_name in first_variants
        for middle in middle_variants
        for last_name in last_variants
    }


def roster_by_period(
    xml_path: Path,
) -> tuple[dict[int, set[str]], dict[int, dict[str, set[str]]]]:
    """Load name variants and all recorded affiliations for each period."""
    names_by_period: dict[int, set[str]] = defaultdict(set)
    parties_by_period: dict[int, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    owners_by_period: dict[int, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    root = ET.parse(xml_path).getroot()
    for member in root.findall("MDB"):
        member_id = member.findtext("ID", "")
        names = set().union(
            *(xml_name_variants(element) for element in member.findall("./NAMEN/NAME"))
        )
        fallback_party = normalize_party(member.findtext("./BIOGRAFISCHE_ANGABEN/PARTEI_KURZ", ""))
        for period_element in member.findall("./WAHLPERIODEN/WAHLPERIODE"):
            period_text = period_element.findtext("WP")
            if not period_text:
                continue
            period = int(period_text)
            names_by_period[period].update(names)
            period_parties = {
                party
                for institution in period_element.findall("./INSTITUTIONEN/INSTITUTION/INS_LANG")
                if institution.text and (party := normalize_party(institution.text)) is not None
            }
            if not period_parties and fallback_party:
                period_parties.add(fallback_party)
            for name in names:
                owners_by_period[period][name].add(member_id)
                parties_by_period[period][name].update(period_parties)
    # Shortened aliases are safe only when they identify one person in-period.
    unique_names = {
        period: {
            name for name in period_names if len(owners_by_period[period][name]) == 1
        }
        for period, period_names in names_by_period.items()
    }
    return unique_names, parties_by_period


@dataclass(frozen=True)
class Resolution:
    name: str
    start: int
    method: str = "exact"


def ocr_spacing_key(value: str) -> str:
    """Normalize only OCR-variable whitespace and hyphens."""
    return re.sub(r"[\s-]+", "", normalize(value)).casefold()


def accent_spacing_key(value: str) -> str:
    """Fold accents after applying the safe OCR spacing normalization."""
    decomposed = unicodedata.normalize("NFKD", normalize(value))
    without_marks = "".join(character for character in decomposed if not unicodedata.combining(character))
    return re.sub(r"[\s-]+", "", without_marks).casefold()


class MemberResolver:
    """Resolve a broad prefix to a member without encoding name syntax in regex."""

    def __init__(self, names: Iterable[str], parties_by_name: dict[str, set[str]]) -> None:
        self.parties_by_name = parties_by_name
        self.normalized = {normalize(name).casefold(): name for name in names}
        self.max_name_length = max((len(name) for name in names), default=1)
        compact_names: dict[str, set[str]] = defaultdict(set)
        accent_names: dict[str, set[str]] = defaultdict(set)
        for name in names:
            compact_names[ocr_spacing_key(name)].add(name)
            accent_names[accent_spacing_key(name)].add(name)
        self.compact_names = compact_names
        self.accent_names = accent_names
        surnames: dict[str, list[str]] = defaultdict(list)
        for name in names:
            surnames[name.split()[-1].casefold()].append(name)
        self.surnames = surnames

    def resolve(self, raw_value: str, party: str | None = None) -> Resolution | None:
        edge_punctuation = " —–-.,;!?()[]{}"
        first = max(0, len(raw_value) - self.max_name_length - 20)

        # Try every suffix beginning at a punctuation/whitespace boundary.
        # This covers extraction joins such as "Pau.Petra Pau".
        for start in range(first, len(raw_value)):
            if start and raw_value[start - 1].isalnum():
                continue
            candidate = normalize(raw_value[start:]).strip(edge_punctuation)
            candidate = re.sub(r"^(?:(?:Prof\.|Dr\.)\s+)+", "", candidate).strip()
            canonical = self.normalized.get(candidate.casefold())
            if canonical:
                return Resolution(canonical, start, "exact")

            # OCR frequently inserts/removes spaces or hyphens inside names.
            # Accept only a unique roster identity under that equivalence.
            compact_candidates = self.compact_names.get(ocr_spacing_key(candidate), set())
            if len(compact_candidates) == 1:
                return Resolution(next(iter(compact_candidates)), start, "ocr_spacing")
            if len(compact_candidates) > 1 and party:
                compatible = [
                    name
                    for name in compact_candidates
                    if party in self.parties_by_name.get(name, set())
                ]
                if len(compatible) == 1:
                    return Resolution(compatible[0], start, "ocr_spacing_party_tiebreak")

            accent_candidates = self.accent_names.get(accent_spacing_key(candidate), set())
            if len(accent_candidates) == 1:
                return Resolution(next(iter(accent_candidates)), start, "accent_spacing")
            if len(accent_candidates) > 1 and party:
                compatible = [
                    name
                    for name in accent_candidates
                    if party in self.parties_by_name.get(name, set())
                ]
                if len(compatible) == 1:
                    return Resolution(compatible[0], start, "accent_spacing_party_tiebreak")

        # A surname alone is accepted only after a real interruption delimiter.
        delimiter = max(raw_value.rfind(character) for character in "(\n\r—–")
        short = normalize(raw_value[delimiter + 1 :]).strip(edge_punctuation) if delimiter >= 0 else ""
        if len(short.split()) != 1:
            return None
        candidates = self.surnames.get(short.casefold(), [])
        if len(candidates) == 1:
            return Resolution(candidates[0], delimiter + 1, "unique_surname")
        if len(candidates) > 1 and party:
            compatible = [name for name in candidates if party in self.parties_by_name.get(name, set())]
            if len(compatible) == 1:
                return Resolution(compatible[0], delimiter + 1, "surname_party_tiebreak")
        return None


@dataclass(frozen=True)
class SpeechHeader:
    start: int
    end: int
    name: str
    party: str


def protocol_period(path: Path) -> int | None:
    match = re.match(r"(\d{1,2})_", path.name)
    return int(match.group(1)) if match else None


def load_text(path: Path) -> str | None:
    with path.open("r", encoding="utf-8") as input_file:
        document = json.load(input_file)
    text = document.get("text")
    if text is None:
        return None
    text = re.sub(r"\n-\n", "-", text)
    text = re.sub(
        r"DIE\s*?LINKE|PDS/\s*?Linke\s*?Liste|PDS/LL|PDS|Die\s*?Linke",
        "DIE LINKE",
        text,
    )
    text = re.sub(r"F\.D\.P\.", "FDP", text)
    alliance_pattern = re.compile(
        r"(BÜND(-\n?)?NIS((-\n?)?SES)?\s*?90/\s*(DIE\s*?)?GRÜ(-\n?)?NEN?)",
        flags=re.UNICODE | re.IGNORECASE,
    )
    return re.sub(alliance_pattern, "GRÜNE", text)


def find_speech_headers(
    text: str,
    resolver: MemberResolver,
    fallback_members: list[tuple[str, str, str]],
) -> list[SpeechHeader]:
    headers: list[SpeechHeader] = []
    for match in SPEECH_SUFFIX_PATTERN.finditer(text):
        field_start = max(0, match.start() - 120)
        raw_field = text[field_start : match.start()]
        party = match.group("party")
        party = "CDU/CSU" if party in {"CDU", "CSU"} else party
        resolution = resolver.resolve(raw_field, party)
        if resolution:
            headers.append(
                SpeechHeader(field_start + resolution.start, match.end(), resolution.name, party)
            )

    # Officials do not always belong to parliament, so retain the old fallback.
    for match in OFFICIAL_SPEAKER_PATTERN.finditer(text):
        raw_name = match.group(1).replace("\n", " ").strip()
        field_start = match.start(1)
        resolution = resolver.resolve(raw_name)
        name = resolution.name if resolution else raw_name
        party = find_party_by_name(name, fallback_members)
        headers.append(SpeechHeader(field_start, match.end(), name, party))

    # Prefer roster-resolved party headers if two alternatives end together.
    unique: dict[tuple[int, int], SpeechHeader] = {}
    for header in sorted(headers, key=lambda item: (item.start, item.end)):
        unique[(header.start, header.end)] = header
    return sorted(unique.values(), key=lambda item: item.start)


def comments_from_text(text: str, resolver: MemberResolver) -> list[dict[str, Any]]:
    comments: list[dict[str, Any]] = []
    searchable = text + "\n"
    for match in INTERRUPTION_SUFFIX_PATTERN.finditer(searchable):
        field_start = max(0, match.start() - 120)
        raw_field = searchable[field_start : match.start()]
        party = match.group("party")
        party = "CDU/CSU" if party in {"CDU", "CSU"} else party
        resolution = resolver.resolve(raw_field, party)
        if resolution is None:
            continue
        end_match = INTERRUPTION_END_PATTERN.search(searchable, match.end())
        if end_match is None:
            continue
        comments.append(
            {
                "commentator": {"name": resolution.name, "party": party},
                "text": searchable[match.end() : end_match.start()].strip(),
                "preceding_context": text[: field_start + resolution.start],
            }
        )
    normalized_text = re.sub("der LINKEN", "DIE LINKE", text)
    for match in CALLOUT_PATTERN.finditer(normalized_text):
        comments.append(
            {
                "commentator": {"name": "<unknown>", "party": match.group(1)},
                "text": match.group(2).strip(),
                "preceding_context": text[: match.start()],
            }
        )
    for match in CALLER_ONLY_ZURUF_PATTERN.finditer(normalized_text):
        annotation = match.group(0)
        zuruf = re.search(r"\bZurufe?\b", annotation)
        if zuruf is None or ":" in annotation[zuruf.end() :]:
            # Spoken callouts are handled by the two extractors above.
            continue

        named_comments = 0
        for party_match in CALLER_ONLY_PARTY_PATTERN.finditer(annotation, zuruf.end()):
            party = party_match.group("bracket_party")
            if party is None:
                continue
            party = "CDU/CSU" if party in {"CDU", "CSU"} else party
            raw_field = annotation[zuruf.end() : party_match.start()]
            resolution = resolver.resolve(raw_field, party)
            if resolution is None:
                continue
            comments.append(
                {
                    "commentator": {"name": resolution.name, "party": party},
                    "text": "",
                    "preceding_context": text[: match.start()],
                }
            )
            named_comments += 1

        if named_comments == 0:
            # Party-only forms such as ``(Zurufe von der AfD)`` have no
            # individual to resolve.  They still represent a caller-only
            # interruption, just like generic spoken callouts do.
            party_match = CALLER_ONLY_PARTY_PATTERN.search(annotation, zuruf.end())
            if party_match:
                party = party_match.group("bracket_party") or party_match.group("plain_party")
                party = "CDU/CSU" if party in {"CDU", "CSU"} else party
                comments.append(
                    {
                        "commentator": {"name": "<unknown>", "party": party},
                        "text": "",
                        "preceding_context": text[: match.start()],
                    }
                )
    return comments


def applause_from_text(text: str) -> dict[str, int]:
    applause = "".join(APPLAUSE_PATTERN.findall(text))
    applause = re.sub("der LINKEN", "DIE LINKE", applause)
    return {party: applause.count(f" {party}") for party in PARTIES}


def parse_protocol(
    source: Path,
    destination: Path,
    members: list[tuple[str, str, str]],
    resolver: MemberResolver,
) -> tuple[int, int, list[tuple[str, str, str]]]:
    """Parse one protocol and write its speech records as JSON."""
    text = load_text(source)
    if text is None:
        print(f"Processed protocol {source.name}. NO TEXT FOUND")
        return 0, 0, []

    headers = find_speech_headers(text, resolver, members)
    speeches: list[dict[str, Any]] = []
    missing_speakers: list[tuple[str, str, str]] = []
    concatenated = 0

    for index, header in enumerate(headers):
        next_start = headers[index + 1].start if index + 1 < len(headers) else len(text)
        name = header.name
        party = header.party
        speech_text = SPEECH_END_PATTERN.split(text[header.end : next_start])[0].strip()
        speech = {
            "speaker": {"name": name, "party": party},
            "text": speech_text,
            "comments": comments_from_text(speech_text, resolver),
            "applause": applause_from_text(speech_text),
        }
        if party not in PARTIES:
            missing_speakers.append((source.name, name, party))
            continue

        if speeches and speeches[-1]["speaker"] == speech["speaker"]:
            previous = speeches[-1]
            previous["text"] += "\n" + speech["text"]
            previous["comments"].extend(speech["comments"])
            previous["applause"] = {
                party_name: previous["applause"][party_name] + speech["applause"][party_name]
                for party_name in PARTIES
            }
            concatenated += 1
        else:
            speeches.append(speech)

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as output_file:
        json.dump(speeches, output_file, ensure_ascii=False, indent=4)
    print(
        f"Processed protocol {source.name}. #speeches = {len(speeches)} "
        f"#speeches_concatenated = {concatenated}"
    )
    return len(speeches), concatenated, missing_speakers


def parse_all_protocols(
    protocol_dir: Path,
    parsed_dir: Path,
    members_path: Path,
    members_xml_path: Path,
    start_from: str | None = None,
) -> list[tuple[str, str, str]]:
    members = load_members(members_path)
    names_by_period, parties_by_period = roster_by_period(members_xml_path)
    sources = sorted(protocol_dir.glob("*.json"))
    if start_from:
        start_name = start_from if start_from.endswith(".json") else f"{start_from}.json"
        matching_sources = [source for source in sources if source.name == start_name]
        if not matching_sources:
            raise ValueError(f"--start-from protocol not found: {start_name}")
        sources = sources[sources.index(matching_sources[0]) :]
    missing_speakers: list[tuple[str, str, str]] = []
    for source in tqdm(sources, desc="Parsing protocols"):
        period = protocol_period(source)
        if period is None or period not in names_by_period:
            print(f"Skipping {source.name}: no Bundestag period roster")
            continue
        resolver = MemberResolver(names_by_period[period], parties_by_period[period])
        _, _, missing = parse_protocol(source, parsed_dir / source.name, members, resolver)
        missing_speakers.extend(missing)
    return missing_speakers


def clean_whitespace(value: str) -> str:
    return " ".join(value.split()).strip()


def build_csv_files(
    parsed_dir: Path,
    interruptions_path: Path,
    speeches_path: Path,
) -> tuple[int, int]:
    """Flatten parsed protocol files into the two analysis CSV datasets."""
    import pandas as pd
    from spacy.lang.de import German

    nlp = German()
    nlp.add_pipe("sentencizer")
    comment_rows: list[list[Any]] = []
    speech_rows: list[list[Any]] = []
    speech_id = 0

    for protocol_path in tqdm(sorted(parsed_dir.glob("*.json")), desc="Building CSVs"):
        with protocol_path.open("r", encoding="utf-8") as input_file:
            protocol = json.load(input_file)
        date = protocol_path.stem[7:]
        for speech in protocol:
            speech_id += 1
            speaker = speech["speaker"]
            sentence_count = sum(1 for _ in nlp(speech["text"]).sents)
            speech_rows.append(
                [speaker["party"], speaker["name"], speech["applause"], sentence_count, date, speech_id]
            )
            for comment in speech.get("comments", []):
                commentator = comment["commentator"]
                comment_rows.append(
                    [
                        comment["text"], commentator["party"], commentator["name"],
                        speaker["party"], speaker["name"], date, sentence_count, speech_id,
                    ]
                )

    interruption_columns = [
        "comment_text", "comment_party", "comment_name", "interrupted_speaker_party",
        "interrupted_speaker", "date", "speech_len_sents", "speech_id",
    ]
    speech_columns = ["speaker_party", "speaker", "applause", "speech_len_sents", "date", "speech_id"]
    interruptions = pd.DataFrame(comment_rows, columns=interruption_columns)
    speeches = pd.DataFrame(speech_rows, columns=speech_columns)

    for column in ("comment_text", "comment_name", "interrupted_speaker"):
        interruptions[column] = interruptions[column].str.replace("\n", " ").apply(clean_whitespace)
    interruptions.loc[interruptions["comment_party"].isin(["CDU", "CSU"]), "comment_party"] = "CDU/CSU"
    interruptions.loc[
        interruptions["interrupted_speaker_party"].isin(["CDU", "CSU"]),
        "interrupted_speaker_party",
    ] = "CDU/CSU"
    speeches["speaker"] = speeches["speaker"].str.replace("\n", " ").apply(clean_whitespace)
    speeches["applause"] = speeches["applause"].apply(json.dumps)

    interruptions_path.parent.mkdir(parents=True, exist_ok=True)
    speeches_path.parent.mkdir(parents=True, exist_ok=True)
    interruptions.to_csv(interruptions_path)
    speeches.to_csv(speeches_path)
    print(f"Wrote {len(interruptions)} interruptions to {interruptions_path}")
    print(f"Wrote {len(speeches)} speeches to {speeches_path}")
    return len(interruptions), len(speeches)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol-dir", type=Path, default=DEFAULT_PROTOCOLS)
    parser.add_argument("--parsed-dir", type=Path, default=DEFAULT_PARSED)
    parser.add_argument("--members", type=Path, default=DEFAULT_MEMBERS)
    parser.add_argument("--members-xml", type=Path, default=DEFAULT_MEMBERS_XML)
    parser.add_argument(
        "--start-from",
        help="Start parsing inclusively at this protocol stem or filename",
    )
    parser.add_argument("--interruptions", type=Path, default=DATA_DIR / "interruptions.csv")
    parser.add_argument("--speeches", type=Path, default=DATA_DIR / "speeches.csv")
    parser.add_argument("--skip-parsing", action="store_true", help="Only rebuild CSVs from parsed JSON")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    if not arguments.skip_parsing:
        parse_all_protocols(
            arguments.protocol_dir,
            arguments.parsed_dir,
            arguments.members,
            arguments.members_xml,
            arguments.start_from,
        )
    build_csv_files(arguments.parsed_dir, arguments.interruptions, arguments.speeches)
