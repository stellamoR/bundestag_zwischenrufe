"""Incrementally refresh dashboard CSVs from recently published DIP protocols."""

from __future__ import annotations

import argparse
import importlib.util
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "_data"
ACQUISITION_DIR = Path(__file__).resolve().parent


def load_script(name: str, filename: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ACQUISITION_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def atomic_csv(frame: pd.DataFrame, destination: Path) -> None:
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    frame.to_csv(temporary, index=False)
    temporary.replace(destination)


def merge_refresh(
    existing: pd.DataFrame,
    fresh: pd.DataFrame,
    refreshed_ids: set[str] | None = None,
    refreshed_dates: set[str] | None = None,
) -> pd.DataFrame:
    """Replace refreshed protocols, falling back to their dates for legacy rows."""
    if "protocol_id" not in existing:
        existing["protocol_id"] = pd.NA
    if refreshed_ids is None:
        refreshed_ids = set(fresh["protocol_id"].dropna().astype(str))
    if refreshed_dates is None:
        refreshed_dates = set(fresh["date"].astype(str))
    old_protocols = existing["protocol_id"].fillna("").astype(str)
    old_dates = existing["date"].astype(str)
    keep = ~old_protocols.isin(refreshed_ids) & ~old_dates.isin(refreshed_dates)
    merged = pd.concat([existing.loc[keep], fresh], ignore_index=True)
    merged["_speech_sort"] = merged["speech_id"].astype(str)
    merged = merged.sort_values(["date", "_speech_sort"], kind="stable")
    return merged.drop(columns="_speech_sort").reset_index(drop=True)


def update_recent_protocols(overlap_days: int = 14, end_date: date | None = None) -> int:
    downloader = load_script("protocol_downloader", "01_get_protocol_data.py")
    parser = load_script("protocol_parser", "03_text_parsing.py")

    speeches_path = DATA_DIR / "speeches.csv"
    interruptions_path = DATA_DIR / "interruptions.csv"
    existing_speeches = pd.read_csv(speeches_path, encoding="utf-8").drop(
        columns=["Unnamed: 0"], errors="ignore"
    )
    existing_interruptions = pd.read_csv(interruptions_path, encoding="utf-8").drop(
        columns=["Unnamed: 0"], errors="ignore"
    )
    latest = max(
        pd.to_datetime(existing_speeches["date"]).max(),
        pd.to_datetime(existing_interruptions["date"]).max(),
    ).date()
    end = end_date or date.today()
    start = min(latest - timedelta(days=overlap_days), end)

    with tempfile.TemporaryDirectory(prefix="bundestag-update-") as temporary:
        work = Path(temporary)
        protocols = work / "protocols"
        parsed = work / "parsed"
        fresh_speeches_path = work / "speeches.csv"
        fresh_interruptions_path = work / "interruptions.csv"

        downloaded = downloader.download_protocols(
            start.isoformat(), end.isoformat(), output_dir=protocols
        )
        if downloaded == 0:
            print(
                f"No protocols with published full text available for {start} through {end}; "
                "nothing to update."
            )
            return 0

        missing = parser.parse_all_protocols(
            protocols,
            parsed,
            DATA_DIR / "abgeordnete.csv",
            DATA_DIR / "MDB_STAMMDATEN.XML",
        )
        if missing:
            print(f"Warning: {len(missing)} speech headers had no supported party mapping.")
        parser.build_csv_files(parsed, fresh_interruptions_path, fresh_speeches_path)

        fresh_speeches = pd.read_csv(fresh_speeches_path, encoding="utf-8").drop(
            columns=["Unnamed: 0"], errors="ignore"
        )
        fresh_interruptions = pd.read_csv(fresh_interruptions_path, encoding="utf-8").drop(
            columns=["Unnamed: 0"], errors="ignore"
        )
        if fresh_speeches.empty:
            raise RuntimeError("Protocols were downloaded but no speeches were parsed; refusing to publish.")
        if fresh_speeches["speech_id"].duplicated().any():
            raise RuntimeError("The refreshed speech IDs are not unique; refusing to publish.")

        expected_protocol_ids = {
            f"{int(path.stem.split('_')[0])}/{int(path.stem.split('_')[1])}"
            for path in protocols.glob("*.json")
        }
        parsed_protocol_ids = set(fresh_speeches["protocol_id"].astype(str))
        missing_protocol_ids = expected_protocol_ids - parsed_protocol_ids
        if missing_protocol_ids:
            raise RuntimeError(
                "No speeches were parsed for protocols "
                f"{sorted(missing_protocol_ids)}; refusing to publish."
            )
        refreshed_dates = set(fresh_speeches["date"].astype(str))

        speeches = merge_refresh(
            existing_speeches, fresh_speeches, parsed_protocol_ids, refreshed_dates
        )
        interruptions = merge_refresh(
            existing_interruptions, fresh_interruptions, parsed_protocol_ids, refreshed_dates
        )
        if len(speeches) < len(existing_speeches) * 0.99:
            raise RuntimeError("Speech count dropped unexpectedly; refusing to publish.")
        if len(interruptions) < len(existing_interruptions) * 0.99:
            raise RuntimeError("Interruption count dropped unexpectedly; refusing to publish.")

        atomic_csv(speeches, speeches_path)
        atomic_csv(interruptions, interruptions_path)
        print(
            f"Updated {downloaded} protocols. Dashboard now contains "
            f"{len(speeches)} speeches and {len(interruptions)} interruptions."
        )
        return downloaded


def parse_args() -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("--overlap-days", type=int, default=14)
    argument_parser.add_argument("--end-date", type=date.fromisoformat)
    return argument_parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    update_recent_protocols(arguments.overlap_days, arguments.end_date)
