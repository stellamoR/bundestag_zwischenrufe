"""Download Bundestag plenary-protocol data from the DIP API."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import requests


API_URL = "https://search.dip.bundestag.de/api/v1/plenarprotokoll-text"
DEFAULT_API_KEY = "R2BZaee.DjdCyihKZMf8AOjtScubP2EVydegzjmBIQ"
DATA_DIR = Path(__file__).resolve().parents[1] / "_data" / "protocols"


def download_protocols(
    start_date: str,
    end_date: str,
    output_dir: Path = DATA_DIR,
    api_key: str = DEFAULT_API_KEY,
) -> int:
    """Download all Bundestag protocols in the inclusive date range."""
    output_dir.mkdir(parents=True, exist_ok=True)
    params: dict[str, Any] = {
        "format": "json",
        "apikey": api_key,
        "f.datum.start": start_date,
        "f.datum.end": end_date,
        "f.zuordnung": "BT",
    }

    document_count = 0
    with requests.Session() as session:
        while True:
            response = session.get(API_URL, params=params, timeout=60)
            response.raise_for_status()
            payload = response.json()

            documents = payload.get("documents", [])
            document_count += len(documents)
            for document in documents:
                period = str(document["wahlperiode"]).zfill(2)
                number = document["dokumentnummer"].split("/")[-1].zfill(3)
                destination = output_dir / f'{period}_{number}_{document["datum"]}.json'
                with destination.open("w", encoding="utf-8") as json_file:
                    json.dump(document, json_file, ensure_ascii=False, indent=4)
                print(destination)

            cursor = payload.get("cursor")
            if cursor is None or cursor == params.get("cursor"):
                break
            params["cursor"] = cursor

    print(f"Retrieved all {document_count} documents")
    return document_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-date", default="1991-03-13")
    parser.add_argument("--end-date", default="2024-06-20")
    parser.add_argument("--output-dir", type=Path, default=DATA_DIR)
    parser.add_argument(
        "--api-key",
        default=os.environ.get("BUNDESTAG_API_KEY", DEFAULT_API_KEY),
        help="DIP API key (defaults to BUNDESTAG_API_KEY, then the notebook key)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    download_protocols(
        arguments.start_date,
        arguments.end_date,
        arguments.output_dir,
        arguments.api_key,
    )
